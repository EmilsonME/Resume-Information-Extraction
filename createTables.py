import sqlite3

conn = sqlite3.connect('testData2.db')
print ("Opened database successfully");

conn.execute('''CREATE TABLE RESUME
         (RESUME_ID INTEGER PRIMARY KEY AUTOINCREMENT,
          CATEGORY  TEXT            NOT NULL,
          FILENAME  TEXT            NOT NULL,
          CONTACT_INFO TEXT                 ,
          EXPECTED TEXT			    );''')

conn.execute('''CREATE TABLE SKILLS
         (SKILL_ID  INTEGER PRIMARY KEY AUTOINCREMENT,
          SKILL     TEXT    		NOT NULL,
          YEARS_OF_XP     INT         ,
          RESUME_ID INTEGER     		NOT NULL,
         	FOREIGN KEY (RESUME_ID) REFERENCES RESUME(RESUME_ID) );''')

conn.execute('''CREATE TABLE EDUCATION
         (EDUCATION_ID INTEGER PRIMARY KEY AUTOINCREMENT,
          DEGREE       TEXT			   NOT NULL,
          RESUME_ID    INTEGER     NOT NULL,
          SCHOOL       TEXT             ,
         	FOREIGN KEY (RESUME_ID) REFERENCES RESUME(RESUME_ID) );''')

conn.execute('''CREATE TABLE EXPERIENCE
         (EXPERIENCE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
          JOB_TITLE     TEXT            NOT NULL,
          DURATION      INT             NOT NULL,
          DESCRIPTION   TEXT                    ,
          RESUME_ID     INTEGER         NOT NULL,
         	FOREIGN KEY (RESUME_ID) REFERENCES RESUME(RESUME_ID) );''')

conn.execute('''CREATE TABLE CERTIFICATION
         (CERT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
          CERT_TITLE   TEXT         ,
          RESUME_ID     INTEGER             NOT NULL,
          FOREIGN KEY (RESUME_ID) REFERENCES RESUME(RESUME_ID) );''')

conn.execute('''CREATE TABLE PROBABILITY
    (PROB_ID  INTEGER PRIMARY KEY AUTOINCREMENT,
    PROB_SD     TEXT            NOT NULL,
    PROB_SE     TEXT            NOT NULL,
    PROB_SA     TEXT            NOT NULL,
    PROB_WD     TEXT            NOT NULL,
    RESUME_ID INTEGER             NOT NULL,
    FOREIGN KEY (RESUME_ID) REFERENCES RESUME(RESUME_ID) );''')

print ("Table created successfully");

conn.close()