import re
import uuid
import django.core.exceptions
from django.shortcuts import render
from Jobapp.validators import validationClass
from rest_framework import viewsets, status
from Jobapp.models import Job, User, Company
from Jobapp.serializers import JobSerializer, UserSerializer, CompanySerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db import ProgrammingError
from django.db.models.expressions import RawSQL
from django.db import connection


# Create your views here.
# this ModelViewSet provides basic crud methods like create, update etc.
class JobViewSets(viewsets.ModelViewSet):
    queryset = Job.objects.all()  # Get all the objects from Database
    serializer_class = JobSerializer

    # Defining filters
    # DjangoFilterBackend allows to use filters in the URL as well (like /api/?company="xyz")
    # SearchFilter means the same except it'll operate on N number of fields but in the url
    # it'll be like (/api/company/?search="xyz")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["company", "location"]

    def list(self, request):
        """Overrided the default list action provided by
        the ModelViewSet, in order to contain a new field
        called 'No of applicants' to the serializer data"""

        # check for the query_params (in case of filter)
        filters = request.query_params
        filtersDict = {}
        if filters:
            for filterName, filterValue in filters.items():
                if filterName in self.filterset_fields:
                    filtersDict[filterName] = filterValue

        # Even if the filtersDict is empty, it returns
        # overall data present in the Job
        jobsData = self.queryset.filter(**filtersDict)

        serializedJobData = self.serializer_class(
            jobsData, many=True, context={"request": request}
        )
        # get number of applicants
        serializedJobData = self.getNumberOfApplicants(serializedJobData)

        return Response(serializedJobData.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        validator = validationClass()
        if not validator.isValidUUID(pk):
            return Response(
                {"message": f"value {pk} isn't a correct id"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # filter based on pk
        jobData = self.queryset.raw("SELECT * FROM Jobapp_job WHERE job_id=%s", [pk])
        serializedJobData = self.serializer_class(jobData, many=True)
        serializedJobData = self.getNumberOfApplicants(serializedJobData)
        return Response(serializedJobData.data, status=status.HTTP_200_OK)

    def getNumberOfApplicants(self, serializedData):
        if not serializedData:
            raise Exception("Serialized data not provided")

        ## Add field to this data
        # count number of applicants
        for eachJobData in serializedData.data:
            job_id = eachJobData.get("job_id")
            # numberOfApplications = User.objects.filter(job_id=job_id).count()
            numberOfApplications = User.objects.filter(
                user_id__in=RawSQL(
                    """
                SELECT user_id FROM Jobapp_user
                WHERE job_id=%s
                """,
                    [job_id],
                )
            ).count()
            eachJobData.update({"Number of Applicants": numberOfApplications})

        return serializedData

    @action(detail=True, methods=["get"])
    def users(self, request, pk=None):
        """API Path: /api/v1/jobs/{pk}/users
        to find out how many users have applied for
        this job using job_id.
        """

        # check if pk's value is a valid UUID
        validator = validationClass()
        checkUUID = validator.isValidUUID(pk)
        if not checkUUID:
            return Response(
                {"message": f"value {pk} isn't a correct id"},
                status=status.HTTP_404_NOT_FOUND,
                content_type="application/json",
            )

        # get the specific job
        jobData = Job.objects.get(pk=pk)
        job_id = jobData.job_id.hex

        # get all the users object
        userData = User.objects.filter(job_id=job_id)
        serializedData = UserSerializer(
            userData, many=True, context={"request": request}
        )
        return Response(serializedData.data)


class UserViewSets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def convertToHex(self, listData):
        print(listData)
        for i in range(len(listData)):
            if isinstance(uuid.UUID(listData[i]), uuid.uuid4):
                listData[i] = listData[i].hex

    # Overriding the create method (used in POST request)
    def create(self, request, *args, **kwargs):
        ## Perform validation for the resume and profile picture
        # resume validation
        validator = validationClass()
        resumeData = request.FILES.get("resume")
        if resumeData:
            validationResult = validator.resumeValidation(resumeData)
            if not validationResult[0]:
                return Response(
                    {"message": validationResult[1]},
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )

        # image validator
        imageData = request.FILES.get("profilePicture")
        if imageData:
            validationResult = validator.ImageValidation(imageData)
            if not validationResult[0]:
                return Response(
                    {"message": validationResult[1]},
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )

        ## Save the data into the database

        # Update the fields
        print(request.data)
        print(self.get_serializer())

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = serializer.validated_data
        headers = self.get_success_headers(data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    # Using this method we can find out which jobs a person has applied so far
    @action(detail=True, methods=["get"])
    def jobs(
        self, request, pk=None
    ):  # pk here means primary key (basically the user_id)
        # here we get the data
        try:
            personData = self.queryset.filter(
                user_id__in=RawSQL(
                    """
                SELECT user_id FROM Jobapp_user
                WHERE user_id=%s
                """,
                    [pk],
                )
            )
            jobId = personData.get().job_id.hex
            # jobsData=Job.objects.filter(job_id=jobId)
            jobsData = Job.objects.filter(
                job_id__in=RawSQL(
                    """
                SELECT job_id FROM Jobapp_job
                WHERE job_id=%s
                """,
                    [jobId],
                )
            )

            # here we serialize the data, for comm.
            serializedJobsData = JobSerializer(
                jobsData, many=True, context={"request": request}
            )
            return Response(serializedJobsData.data)
        except django.core.exceptions.ObjectDoesNotExist:
            return Response(
                {"message": f"person id '{pk}' doesn't exist"},
                content_type="application/json",
            )


class CompanyViewSets(viewsets.ModelViewSet):
    queryset = Company.objects.all()  # get all the data of company from db
    serializer_class = CompanySerializer

    # Basic filters
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "location"]

    @action(detail=False, methods=["get"])
    def jobs(self, request):
        serializedCompanyData = self.serializer_class(self.get_queryset(), many=True)
        for eachData in serializedCompanyData.data:
            companyId = eachData.get("company_id")

            # get jobs data by company_id from database
            # .values() returns the QuerySet
            # jobData = Job.objects.filter(company=companyId).values()
            jobData = Job.objects.filter(
                job_id__in=RawSQL(
                    """
                SELECT job_id from Jobapp_job
                WHERE company_id=%s
                """,
                    [companyId],
                )
            ).values()
            eachData.update({"Jobs": jobData})

        return Response(serializedCompanyData.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def users(self, request):
        serializedCompanyData = self.serializer_class(self.get_queryset(), many=True)
        for eachData in serializedCompanyData.data:
            company_id = eachData.get("company_id")

            # Get user information by company_id from database
            userData = User.objects.filter(
                user_id__in=RawSQL(
                    """
                SELECT user_id from Jobapp_user
                WHERE company_id=%s
                """,
                    [company_id],
                )
            ).values()
            eachData.update({"User": userData})

        return Response(serializedCompanyData.data, status=status.HTTP_200_OK)
