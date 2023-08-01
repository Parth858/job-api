Open the job file 
launch the virtual env : myenv\scripts\activate 
Run : python manage.py migrate (if any migrations are neended)
      python manage.py makemigrations
      python manage.py runserver (follow the link provided on the page)

* APIs related code is present in Jobapp/
* APIs avialable
  1. Company (/api/v1/company)    
  Filters: name, location     
  Actions avialable:
      /api/v1/company/{company_id} : Show details of a specific job    
      /api/v1/company/jobs : Show number of jobs available in N number of companies     
      /api/v1/company/users: Show number of users available in N number of companies

  2. Jobs (/api/v1/jobs)    
  Filters: company, location    
  Actions avialable: 
      /api/v1/jobs/{job_id}: Show details of a specific job    
      /api/v1/jobs/{job_id}/users: Show users applied for a specific job 
    
  3. User (/api/v1/user)    
  Filters: NA    
  Actions available:    
      /api/v1/user/{user_id}: Show details of a specific user    
      /api/v1/user/{user_id}/jobs: Show number of jobs applied by a specific user    
