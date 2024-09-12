from django.db import connection
import xlwt
from datetime import datetime

def convertDates(year, quarter):
    if quarter == "1":
        startDate = str(year)+"-01-01"
        endDate = str(year)+"-03-31"
    elif quarter == "2":
        startDate = str(year)+"-04-01"
        endDate = str(year)+"-06-30"
    elif quarter == "3":
        startDate = str(year)+"-07-01"
        endDate = str(year)+"-09-30"
    elif quarter == "4" :
        startDate = str(year)+"-10-01"
        endDate = str(year)+"-12-31"
    else:
        startDate = "0000-00-00"
        endDate = "0000-00-00"

    return {'startDate' : startDate, 'endDate' : endDate}


# def departmentReport(startDate, endDate):
    
    
     
#     with connection.cursor() as cursor:
#         query = "SELECT account_user.department_code AS department, Count( DISTINCT project_project.id) AS projects, Count( DISTINCT publication_publication.id) AS publications, Count(DISTINCT innovation_innovation.id) AS innovations FROM account_user LEFT JOIN ( SELECT * FROM project_project WHERE date_from <= '"+endDate+"' AND expected_completion_date >= '"+startDate+"' ) AS project_project  ON project_project.user_id =  account_user.id LEFT JOIN  (SELECT * FROM publication_publication WHERE created_at::date >= '"+startDate+"' AND created_at::date <= '"+endDate+"') AS publication_publication ON publication_publication.author_id = account_user.id LEFT JOIN (SELECT * FROM innovation_innovation WHERE created_at::date >= '"+startDate+"' AND created_at::date <= '"+endDate+"') AS innovation_innovation ON innovation_innovation.user_id = account_user.id WHERE (publication_publication.is_approved = TRUE OR publication_publication.id IS NULL ) AND account_user.department_code IS NOT NULL GROUP BY account_user.department_code "
#         cursor.execute(query);
        
#         columns = [col[0] for col in cursor.description]
#         report = [dict(zip(columns, row)) for row in cursor.fetchall()]
    

#     return  report

def staffReport(startDate, endDate):
    
    
     
    with connection.cursor() as cursor:
        query = f"SELECT * FROM (SELECT account_user.id, account_user.title,  concat( first_name, ' ', last_name) AS fullname, account_user.department_code AS department_code, Count( DISTINCT project_project.id) AS projects, Count( DISTINCT publication_publication.id) AS publications, Count(DISTINCT innovation_innovation.id) AS innovations FROM account_user LEFT JOIN ( SELECT * FROM project_project WHERE date_from <= '{endDate}' AND expected_completion_date >= '{startDate}' ) AS project_project  ON project_project.user_id =  account_user.id LEFT JOIN (SELECT * FROM publication_publication WHERE created_at::date >= '{startDate}' AND created_at::date <= '{endDate}') AS publication_publication ON publication_publication.author_id = account_user.id LEFT JOIN (SELECT * FROM innovation_innovation WHERE created_at::date >= '{startDate}' AND created_at::date <= '{endDate}') AS innovation_innovation ON innovation_innovation.user_id = account_user.id WHERE (publication_publication.is_approved = TRUE OR publication_publication.id IS NULL )  GROUP BY account_user.id) AS temp WHERE publications > 0 OR innovations > 0 OR projects > 0"
        cursor.execute(query);
        
        columns = [col[0] for col in cursor.description]
        report = [dict(zip(columns, row)) for row in cursor.fetchall()]
    

    return  report


def departmentReport(year = None):
    if(year is None):
        with connection.cursor() as cursor:
            query = f"SELECT organisation_department.name AS department, organisation_faculty.name AS faculty, Count( DISTINCT project_project.id) AS projects, Count( DISTINCT publication_publication.id) AS publications, Count(DISTINCT innovation_innovation.id) AS innovations FROM organisation_faculty LEFT JOIN organisation_department ON organisation_faculty.id = organisation_department.faculty_id LEFT JOIN account_user ON organisation_department.code = account_user.department_code LEFT JOIN project_project  ON project_project.user_id =  account_user.id LEFT JOIN  publication_publication ON publication_publication.author_id = account_user.id LEFT JOIN innovation_innovation ON innovation_innovation.user_id = account_user.id WHERE (publication_publication.is_approved = TRUE OR publication_publication.id IS NULL )  GROUP BY organisation_department.name, organisation_faculty.name ORDER BY organisation_faculty.name, organisation_department.name"
            cursor.execute(query);
            
            columns = [col[0] for col in cursor.description]
            report = [dict(zip(columns, row)) for row in cursor.fetchall()]
        print("All Time")
    else:
        with connection.cursor() as cursor:
            query = f"SELECT organisation_department.name AS department, organisation_faculty.name AS faculty, Count( DISTINCT project_project.id) AS projects, Count( DISTINCT publication_publication.id) AS publications, Count(DISTINCT innovation_innovation.id) AS innovations FROM organisation_faculty LEFT JOIN organisation_department ON organisation_faculty.id = organisation_department.faculty_id LEFT JOIN account_user ON organisation_department.code = account_user.department_code LEFT JOIN (SELECT * FROM project_project WHERE DATE_PART('Year', date_from) <= '{year}' AND DATE_PART('Year', expected_completion_date) >= '{year}') AS project_project  ON project_project.user_id =  account_user.id LEFT JOIN (SELECT * FROM publication_publication WHERE year_of_publication = '{year}') AS  publication_publication ON publication_publication.author_id = account_user.id LEFT JOIN (SELECT * FROM innovation_innovation WHERE year_of_innovation  = '{year}') AS innovation_innovation ON innovation_innovation.user_id = account_user.id WHERE (publication_publication.is_approved = TRUE OR publication_publication.id IS NULL )  GROUP BY organisation_department.name, organisation_faculty.name ORDER BY organisation_faculty.name, organisation_department.name"
            cursor.execute(query);
            
            columns = [col[0] for col in cursor.description]
            report = [dict(zip(columns, row)) for row in cursor.fetchall()]
        print(year)
    return report

def facultyReport(year = None):
    if(year is None):
        with connection.cursor() as cursor:
            query = f"SELECT organisation_faculty.name AS faculty, Count( DISTINCT project_project.id) AS projects, Count( DISTINCT publication_publication.id) AS publications, Count(DISTINCT innovation_innovation.id) AS innovations FROM organisation_faculty LEFT JOIN organisation_department ON organisation_faculty.id = organisation_department.faculty_id LEFT JOIN account_user ON organisation_department.code = account_user.department_code LEFT JOIN project_project  ON project_project.user_id =  account_user.id LEFT JOIN  publication_publication ON publication_publication.author_id = account_user.id LEFT JOIN innovation_innovation ON innovation_innovation.user_id = account_user.id WHERE (publication_publication.is_approved = TRUE OR publication_publication.id IS NULL )  GROUP BY organisation_faculty.name"
            cursor.execute(query);
            
            columns = [col[0] for col in cursor.description]
            report = [dict(zip(columns, row)) for row in cursor.fetchall()]
        print("All Time")
    else:
        with connection.cursor() as cursor:
            query = f"SELECT organisation_faculty.name AS faculty, Count( DISTINCT project_project.id) AS projects, Count( DISTINCT publication_publication.id) AS publications, Count(DISTINCT innovation_innovation.id) AS innovations FROM organisation_faculty LEFT JOIN organisation_department ON organisation_faculty.id = organisation_department.faculty_id LEFT JOIN account_user ON organisation_department.code = account_user.department_code LEFT JOIN (SELECT * FROM project_project WHERE DATE_PART('Year', date_from) <= '{year}' AND DATE_PART('Year', expected_completion_date) >= '{year}') AS project_project  ON project_project.user_id =  account_user.id LEFT JOIN (SELECT * FROM publication_publication WHERE year_of_publication = '{year}') AS  publication_publication ON publication_publication.author_id = account_user.id LEFT JOIN (SELECT * FROM innovation_innovation WHERE year_of_innovation  = '{year}') AS innovation_innovation ON innovation_innovation.user_id = account_user.id WHERE (publication_publication.is_approved = TRUE OR publication_publication.id IS NULL )  GROUP BY organisation_faculty.name"
            cursor.execute(query);
            
            columns = [col[0] for col in cursor.description]
            report = [dict(zip(columns, row)) for row in cursor.fetchall()]
        print(year)
    return report

def facultyProjectReport(year = None):
    if(year is None):
        with connection.cursor() as cursor:
            query = f"SELECT organisation_faculty.name AS faculty, organisation_department.name as department, CONCAT(account_user.title, ' ', account_user.first_name, ' ', account_user.last_name) as Fullname, project_project.title AS project_title, project_project.description as description, date_from, expected_completion_date FROM organisation_faculty JOIN organisation_department ON organisation_faculty.id = organisation_department.faculty_id JOIN account_user ON organisation_department.code = account_user.department_code JOIN project_project  ON project_project.user_id =  account_user.id ORDER BY faculty, department, Fullname"
            cursor.execute(query);
            
            columns = [col[0] for col in cursor.description]
            report = [dict(zip(columns, row)) for row in cursor.fetchall()]
        print("All Time")
    else:
        with connection.cursor() as cursor:
            query = f"SELECT organisation_faculty.name AS faculty, organisation_department.name as department, CONCAT(account_user.title, ' ', account_user.first_name, ' ', account_user.last_name) as Fullname, project_project.title AS project_title, project_project.description as description, date_from, expected_completion_date FROM organisation_faculty JOIN organisation_department ON organisation_faculty.id = organisation_department.faculty_id JOIN account_user ON organisation_department.code = account_user.department_code JOIN project_project  ON project_project.user_id =  account_user.id WHERE DATE_PART('Year', date_from) <= '{year}' AND DATE_PART('Year', expected_completion_date) >= '{year}' ORDER BY faculty, department, Fullname"
            cursor.execute(query);
            
            columns = [col[0] for col in cursor.description]
            report = [dict(zip(columns, row)) for row in cursor.fetchall()]
        print(year)
    return report



def facultyPublicationReport(year = None):
    if(year is None):
        with connection.cursor() as cursor:
            query = f"SELECT organisation_faculty.name AS faculty, organisation_department.name as department, CONCAT(account_user.title, ' ', account_user.first_name, ' ', account_user.last_name) as Fullname, publication_publication.title AS publication_title, publication_publication.publication_type, publication_publication.year_of_publication, publication_publication.abstract as abstract FROM organisation_faculty JOIN organisation_department ON organisation_faculty.id = organisation_department.faculty_id JOIN account_user ON organisation_department.code = account_user.department_code JOIN publication_publication  ON publication_publication.author_id =  account_user.id WHERE publication_publication.is_approved = TRUE ORDER BY faculty, department, Fullname"
            cursor.execute(query);
            
            columns = [col[0] for col in cursor.description]
            report = [dict(zip(columns, row)) for row in cursor.fetchall()]
        print("All Time")
    else:
        with connection.cursor() as cursor:
            query = f"SELECT organisation_faculty.name AS faculty, organisation_department.name as department, CONCAT(account_user.title, ' ', account_user.first_name, ' ', account_user.last_name) as Fullname, publication_publication.title AS publication_title, publication_publication.publication_type, publication_publication.year_of_publication, publication_publication.abstract as abstract FROM organisation_faculty JOIN organisation_department ON organisation_faculty.id = organisation_department.faculty_id JOIN account_user ON organisation_department.code = account_user.department_code JOIN publication_publication  ON publication_publication.author_id =  account_user.id WHERE publication_publication.is_approved = TRUE AND publication_publication.year_of_publication = '{year}' ORDER BY faculty, department, Fullname"
            cursor.execute(query);
            
            columns = [col[0] for col in cursor.description]
            report = [dict(zip(columns, row)) for row in cursor.fetchall()]
        print(year)
    return report



def facultyInnovationReport(year = None):
    if(year is None):
        with connection.cursor() as cursor:
            query = f"SELECT organisation_faculty.name AS faculty, organisation_department.name as department, CONCAT(account_user.title, ' ', account_user.first_name, ' ', account_user.last_name) as Fullname, innovation_innovation.title AS innovation_title, innovation_innovation.description, innovation_innovation.year_of_innovation FROM organisation_faculty JOIN organisation_department ON organisation_faculty.id = organisation_department.faculty_id JOIN account_user ON organisation_department.code = account_user.department_code JOIN innovation_innovation  ON innovation_innovation.user_id =  account_user.id ORDER BY faculty, department, Fullname"
            cursor.execute(query);
            
            columns = [col[0] for col in cursor.description]
            report = [dict(zip(columns, row)) for row in cursor.fetchall()]
        print("All Time")
    else:
        with connection.cursor() as cursor:
            query = f"SELECT organisation_faculty.name AS faculty, organisation_department.name as department, CONCAT(account_user.title, ' ', account_user.first_name, ' ', account_user.last_name) as Fullname, innovation_innovation.title AS innovation_title, innovation_innovation.description, innovation_innovation.year_of_innovation FROM organisation_faculty JOIN organisation_department ON organisation_faculty.id = organisation_department.faculty_id JOIN account_user ON organisation_department.code = account_user.department_code JOIN innovation_innovation  ON innovation_innovation.user_id =  account_user.id WHERE innovation_innovation.year_of_innovation = '{year}' ORDER BY faculty, department, Fullname"
            cursor.execute(query);
            
            columns = [col[0] for col in cursor.description]
            report = [dict(zip(columns, row)) for row in cursor.fetchall()]
        print(year)
    return report



