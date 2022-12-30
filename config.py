from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.abspath(os.path.dirname(__file__)), '.env'))

imagePath=r"/home/genshinimpact1234/mysite/server/others/images" 

#Google variabables
CLIENT_ID=os.environ['CLIENT_ID']
CLIENT_SECRET=os.environ['CLIENT_SECRET']
REDIRECT_URI = os.environ['REDIRECT_URI']
SCOPE=['https://www.googleapis.com/auth/drive']
CLIENT_SECRET_FILE=r'/home/genshinimpact1234/mysite/server/token.json'
API_NAME='drive'
API_VERSION='v3'

service_folder="14goVz8uN-1xFF0SXU3hXfma5JP-ChpWg"
item_folder="1lJOhun8DjYi1MG1YbVaZwBQ_BoKhWowU"
init_customerfolder="1YXImIQ6lHuvh4zz_T5efUuTEa3OiDT82"
init_employeefolder="1SXn50CvDGEIKR588SF8E1UJjCd2oruOX"
init_imageFolder="1m2WWFI8YOSqBuWUiBqTD4BFyh96dvFSH"
final_customerfolder="159GJ0N1Tgzh4_0ww16w_CDWUCkyeX7ni"
final_employeefolder="1xiz5KJQLAZ8IAGGktse3YpuNJG3t94vN"
final_imageFolder="151c1-LG6q9hkpoybJwzxUymYrzjCe_YS"

# service_folder="1WAGNXHGxHZd5Jgb7pbt2LVb27qhod8dw"
# item_folder="1WAGNXHGxHZd5Jgb7pbt2LVb27qhod8dw"
# init_customerfolder="1WAGNXHGxHZd5Jgb7pbt2LVb27qhod8dw"
# init_employeefolder="1WAGNXHGxHZd5Jgb7pbt2LVb27qhod8dw"
# init_imageFolder="1WAGNXHGxHZd5Jgb7pbt2LVb27qhod8dw"
# final_customerfolder="1WAGNXHGxHZd5Jgb7pbt2LVb27qhod8dw"
# final_employeefolder="1WAGNXHGxHZd5Jgb7pbt2LVb27qhod8dw"
# final_imageFolder="1WAGNXHGxHZd5Jgb7pbt2LVb27qhod8dw"



class ApplicationConfig:

    # JWT_SECRET_KEY = "sdfsdf123213213" #os.environ['SECRET_KEY']
    SECRET_KEY=os.environ['SECRET_KEY'] #Secert key for session

    #SQL config
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="genshinimpact123",
    password="menava555",
    hostname="genshinimpact1234.mysql.pythonanywhere-services.com",
    databasename="genshinimpact123$flask",
)
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    # SQLALCHEMY_DATABASE_URI = f"mysql + mysqldb://root@{os.environ['PUBLIC_IP_ADDRESS']}/{os.environ['DBNAME']}?unix_socket =/cloudsql/{os.environ['PROJECT_ID']}:{os.environ['INSTANCE_NAME']}"
    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root@35.188.202.193/flask?unix_socket=/cloudsql/nice-flask:nice-workshop'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #Session Config
    # SESSION_TYPE='sqlalchemy'
    # SESSION_SQLALCHEMY=db
    # SESSION_COOKIE_SAMESITE="None"
    # SESSION_COOKIE_SECURE=True