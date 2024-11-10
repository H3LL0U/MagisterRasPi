import login
from credentials import *
from MagisterPy import MagisterSession
import schedule
def main():
    while True:
        session = None
        while not check_for_saved_credentials():


        
            login_page = login.LoginPage()
            if login_page.session.app_auth_token:
            
                save_new_credentials(login_page.SCHOOL_NAME,login_page.USERNAME,login_page.PASSWORD)
                session = login_page.session
            else:
                return
        saved_credentials = get_saved_credentials()
        if not session:
            session= MagisterSession()
            session.login(school_name=saved_credentials[0],username=saved_credentials[1],password=saved_credentials[2])
        
        main_app = schedule.TimetableApp(session)
        main_app.mainloop()
        if not main_app._logged_out:
            break
    

if __name__ == "__main__":
    main()

        