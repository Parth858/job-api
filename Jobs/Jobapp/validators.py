import re
import uuid


class validationClass:
    """This class aims at providing
    validation functionality for multiple stuff,
    right now it only supports
    1. Resume file
    2. Image file
    """

    def isValidUUID(self, value):
        # Expects value in hex format of uuid
        try:
            uuidValue = uuid.UUID(str(value))
        except ValueError:
            return False
        else:
            return str(uuidValue.hex) == str(value)

    def ImageValidation(self, imageFile):
        # check size
        filesize = imageFile.size / (1024 * 1024)
        if filesize > 10:
            return (False, "Profile Image shouldn't exceed 10mb")
        else:
            allowedImageExtensions = ["png", "jpeg", "jpg"]
            allowedContentTypes = ["image/png", "image/jpg", "image/jpeg"]
            imageFileExtension = imageFile.name.split(".")[-1].lower()
            uploadFileToStorage = False

            # filename check
            if not re.match("[\w\-]+\.\w{3,4}$", imageFile.name):
                return (False, "Image File name isn't appropriate")

            # Allowed content-type/extensions check
            if (
                imageFileExtension in allowedImageExtensions
                and imageFile.content_type in allowedContentTypes
            ):
                # check signatures
                if imageFileExtension == "png":
                    if imageFile.file.read()[:8].hex().upper().encode(
                        "ASCII"
                    ) == "89504E470D0A1A0A".encode("ASCII"):
                        uploadFileToStorage = True
                elif imageFileExtension == "jpg" or imageFileExtension == "jpeg":
                    if imageFile.file.read()[:8].hex().upper().startswith("FFD8"):
                        uploadFileToStorage = True
                else:
                    return (False, "Image File type isn't supported")
            else:
                return (False, "Oops, Wrong Image file submitted")

        if uploadFileToStorage:
            return (True, "File is valid")

    def resumeValidation(self, resumeFile):
        # check size (shouldn't exceed 10mb)
        filesize = resumeFile.size / (1024 * 1024)
        if filesize > 10:
            return (False, "Resume File size shouldn't exceed 10mb")
        else:
            ## check characters present in the file name
            # for example: Only allowed those files that
            # includes only alphanumeric, hyphen and a period
            if not re.match("[\w\-]+\.\w{3,4}$", resumeFile.name):
                return (False, "Resume File name isn't appropriate")

            # check file extension & content_type
            uploadFileToStorage = False
            allowedFileExtensions = ["pdf", "docx", "doc"]
            allowedContentTypes = [
                "application/pdf",
                "application/msword",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ]
            fileExtension = resumeFile.name.split(".")[-1].lower()
            if (
                fileExtension in allowedFileExtensions
                and resumeFile.content_type in allowedContentTypes
            ):
                # check file signature thing
                if fileExtension == "pdf":
                    if resumeFile.file.read()[:4].hex().upper().encode(
                        "ASCII"
                    ) == "25504446".encode("ASCII"):
                        uploadFileToStorage = True
                elif fileExtension == "docx":
                    if resumeFile.file.read()[:4].hex().upper().encode(
                        "ASCII"
                    ) == "504B0304".encode("ASCII"):
                        uploadFileToStorage = True
                elif fileExtension == "doc":
                    if resumeFile.file.read()[:4].hex().upper().encode(
                        "ASCII"
                    ) == "D0CF11E0A1B11AE1".encode("ASCII"):
                        uploadFileToStorage = True
                else:
                    return (False, "Resume File type is not supported")
            else:
                return (False, "Oops, wrong resume file submitted")

        if uploadFileToStorage:
            return (True, "File is valid")
