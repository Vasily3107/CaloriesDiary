from tkinter     import Tk, Label, Button, Entry, Listbox, messagebox, Canvas
from tkinter.ttk import Notebook, Frame, Combobox

from db_handler  import DBHandler

root = Tk()
tab_switch = Notebook(root)

current_email = None
sex_values = ['M', 'F']
goal_values = ['Lose weight', 'Stay fit', 'Gain weight']

def log_in_sign_up_trigger(email):
    global current_email
    current_email = email
    update_meal_list()
    update_act_list()
    update_user_settings_displays()
    update_progress_info()
    tab_switch.add(progress_frame,text='Progress')
    tab_switch.add(meal_frame,    text='Meals')
    tab_switch.add(act_frame,     text='Activities')
    tab_switch.add(profile_frame, text='Profile')

# - - - log in page - - - - - - - - - - - - - - - - - - - - - - - -
log_in_frame = Frame(tab_switch)

log_in_email_label = Label(log_in_frame, text='Email:')
log_in_email_entry = Entry(log_in_frame)

log_in_password_label = Label(log_in_frame, text='Password:')
log_in_password_entry = Entry(log_in_frame, show='*')

def log_in_command():
    email    = log_in_email_entry.get()
    password = log_in_password_entry.get()

    if len(email) < 1 or len(email) > 320:
        log_in_info_label.config(text='Email limits are [1; 320]', fg='red')
        return

    if len(password) < 1 or len(password) > 20:
        log_in_info_label.config(text='Password limits are [1; 20]', fg='red')
        return

    if not DBHandler.log_in(email, password):
        log_in_info_label.config(text='Invalid email or password', fg='red')
        return

    log_in_info_label.config(text='Loged in', fg='green')
    log_in_sign_up_trigger(email)

log_in_button = Button(log_in_frame, text='Log in', command=log_in_command)
log_in_info_label = Label(log_in_frame, text='')

log_in_email_label   .grid(row=0, column=0)
log_in_email_entry   .grid(row=0, column=1)
log_in_password_label.grid(row=1, column=0)
log_in_password_entry.grid(row=1, column=1)
log_in_button        .grid(row=2, column=0, columnspan=2)
log_in_info_label    .grid(row=3, column=0, columnspan=2)

# - - - sign up page - - - - - - - - - - - - - - - - - - - - - - - -
sign_up_frame = Frame(tab_switch)

sign_up_email_label = Label(sign_up_frame, text='Email:')
sign_up_email_entry = Entry(sign_up_frame)

sign_up_password_label = Label(sign_up_frame, text='Password:')
sign_up_password_entry = Entry(sign_up_frame, show='*')

sign_up_confirm_password_label = Label(sign_up_frame, text='Confirm\npassword:')
sign_up_confirm_password_entry = Entry(sign_up_frame, show='*')

sign_up_sex_label = Label(sign_up_frame, text='Sex:')
sign_up_sex_entry = Combobox(sign_up_frame, state='readonly', values=sex_values)
sign_up_sex_entry.set(sex_values[0])

sign_up_age_label = Label(sign_up_frame, text='Age:')
sign_up_age_entry = Entry(sign_up_frame)

sign_up_weight_label = Label(sign_up_frame, text='Weight:')
sign_up_weight_entry = Entry(sign_up_frame)

sign_up_height_label = Label(sign_up_frame, text='Height:')
sign_up_height_entry = Entry(sign_up_frame)

sign_up_goal_label = Label(sign_up_frame, text='Your goal:')
sign_up_goal_entry = Combobox(sign_up_frame, state='readonly', values=goal_values)
sign_up_goal_entry.set(goal_values[0])

def sign_up_command():
    email    = sign_up_email_entry.get()
    password = sign_up_password_entry.get()
    conf_pas = sign_up_confirm_password_entry.get()
    sex      = sign_up_sex_entry.get()
    age      = sign_up_age_entry.get()
    weight   = sign_up_weight_entry.get()
    height   = sign_up_height_entry.get()
    goal     = sign_up_goal_entry.get()

    if len(email) < 1 or len(email) > 320:
        sign_up_info_label.config(text='Email limits are [1; 320]', fg='red'); return

    if len(password) < 1 or len(password) > 20:
        sign_up_info_label.config(text='Password limits are [1; 20]', fg='red'); return
    if password != conf_pas:
        sign_up_info_label.config(text='Entered passwords do NOT match', fg='red'); return

    try: age = int(age)
    except:     sign_up_info_label.config(text='Age should be a positive integer', fg='red'); return
    if age < 0: sign_up_info_label.config(text='Age should be a positive integer', fg='red'); return

    try: weight = int(weight)
    except:        sign_up_info_label.config(text='Weight should be a positive integer', fg='red'); return
    if weight < 0: sign_up_info_label.config(text='Weight should be a positive integer', fg='red'); return

    try: height = int(height)
    except:        sign_up_info_label.config(text='Height should be a positive integer', fg='red'); return
    if height < 0: sign_up_info_label.config(text='Height should be a positive integer', fg='red'); return

    if not DBHandler.sign_up(email, password, sex, age, weight, height, goal):
        sign_up_info_label.config(text='User with this email already exists', fg='red'); return

    sign_up_info_label.config(text='Signed up', fg='green')
    log_in_sign_up_trigger(email)

sign_up_button = Button(sign_up_frame, text='Sign up', command=sign_up_command)
sign_up_info_label = Label(sign_up_frame, text='')

sign_up_email_label           .grid(row=0, column=0)
sign_up_email_entry           .grid(row=0, column=1)
sign_up_password_label        .grid(row=1, column=0)
sign_up_password_entry        .grid(row=1, column=1)
sign_up_confirm_password_label.grid(row=2, column=0)
sign_up_confirm_password_entry.grid(row=2, column=1)
sign_up_button                .grid(row=3, column=0, columnspan=2)
sign_up_info_label            .grid(row=4, column=0, columnspan=2)

sign_up_sex_label   .grid(row=0, column=2)
sign_up_sex_entry   .grid(row=0, column=3)
sign_up_age_label   .grid(row=1, column=2)
sign_up_age_entry   .grid(row=1, column=3)
sign_up_weight_label.grid(row=2, column=2)
sign_up_weight_entry.grid(row=2, column=3)
sign_up_height_label.grid(row=3, column=2)
sign_up_height_entry.grid(row=3, column=3)
sign_up_goal_label  .grid(row=4, column=2)
sign_up_goal_entry  .grid(row=4, column=3)

# - - - progress page - - - - - - - - - - - - - - - - - - - - - - - -
progress_frame = Frame(tab_switch)

def calculate_calories() -> int:
    *_, sex, age, weight, height, goal = DBHandler.get_user_info(current_email)

    goal_factor = 0.5 * (goal_values[::-1].index(goal) + 1)

    if sex == 'F': return int(655.1 + (9.563 * weight) + (1.85 * height) - (4.676 * age)) * goal_factor
    else:          return int(66.5 + (13.75 * weight) + (5.003 * height) - (6.775 * age)) * goal_factor

def update_progress_info():
    calories_score, goals_met, *_, goal = DBHandler.get_user_info(current_email)

    calculated_calories = calculate_calories()

    if calories_score >= calculated_calories:
        calories_score %= calculated_calories
        DBHandler.update_user_scores(calories_score, current_email)

    progress_goals_met_label     .config(text=f'Goals met: {goals_met}')
    progress_calories_score_label.config(text=f'Calories score: {calories_score} / {calculated_calories} ({round(100*calories_score/calculated_calories, 2)}%)')
    progress_total_score_label   .config(text=f'Toatal score: {goals_met * calories_score}')
    progress_goal_label          .config(text=f'Goal: {goal}')

    ratio_angle = 360 * calories_score / calculated_calories
    pie_chart.delete('all')
    pie_chart.create_oval((1, 1, 200, 200), fill='grey', outline='')
    pie_chart.create_arc((1, 1, 200, 200), fill=('blue' if ratio_angle > 0 else 'red'), extent=ratio_angle, outline='')

progress_goals_met_label      = Label(progress_frame, text='')
progress_calories_score_label = Label(progress_frame, text='')
progress_total_score_label    = Label(progress_frame, text='')
progress_goal_label           = Label(progress_frame, text='')

pie_chart = Canvas(progress_frame, width=200)

progress_goals_met_label.pack()
progress_calories_score_label.pack()
progress_total_score_label.pack()
progress_goal_label.pack()
pie_chart.pack()

# - - - meal page - - - - - - - - - - - - - - - - - - - - - - - -
meal_frame = Frame(tab_switch)

meal_name_label = Label(meal_frame, text='Name:')
meal_name_entry = Entry(meal_frame)

meal_calories_label = Label(meal_frame, text='Calories:')
meal_calories_entry = Entry(meal_frame)

def update_meal_list():
    global current_email
    meal_list.delete(0, 'end')
    for name, calories, time in DBHandler.meal_iter(current_email):
        meal_list.insert('end', f'{name} with {calories} calories on {time}')

def add_meal_command():
    name = meal_name_entry.get()
    calories = meal_calories_entry.get()

    if len(name) == 0 or len(name) > 100:
        meal_info_label.config(text='Meal name limits are [1; 100]', fg='red'); return

    try: calories = int(calories)
    except:          meal_info_label.config(text='Meal calories must be a positive integer', fg='red'); return
    if calories < 0: meal_info_label.config(text='Meal calories must be a positive integer', fg='red'); return

    DBHandler.add_meal(current_email, name, calories)
    update_meal_list()
    update_progress_info()

meal_add_button = Button(meal_frame, text='Add meal and Update list', command=add_meal_command)
meal_info_label = Label(meal_frame, text='')
meal_list = Listbox(meal_frame, width=90, height=15, selectmode='single')

meal_name_label    .grid(row=0, column=0)
meal_name_entry    .grid(row=0, column=1)
meal_calories_label.grid(row=1, column=0)
meal_calories_entry.grid(row=1, column=1)
meal_add_button    .grid(row=2, column=0, columnspan=2)
meal_info_label    .grid(row=3, column=0, columnspan=2)
meal_list          .place(y=100, x=5)

# - - - activities page - - - - - - - - - - - - - - - - - - - - - - - -
act_frame = Frame(tab_switch)

act_name_label = Label(act_frame, text='Name:')
act_name_entry = Entry(act_frame)

act_calories_label = Label(act_frame, text='Calories:')
act_calories_entry = Entry(act_frame)

def update_act_list():
    global current_email
    act_list.delete(0, 'end')
    for name, calories, time in DBHandler.activity_iter(current_email):
        act_list.insert('end', f'Did {name} and burned {calories} calories on {time}')

def add_act_command():
    name = act_name_entry.get()
    calories = act_calories_entry.get()

    if len(name) == 0 or len(name) > 100:
        act_info_label.config(text='Activity name limits are [1; 100]', fg='red'); return

    try: calories = int(calories)
    except:          act_info_label.config(text='Activity calories must be a positive integer', fg='red'); return
    if calories < 0: act_info_label.config(text='Activity calories must be a positive integer', fg='red'); return

    DBHandler.add_activity(current_email, name, calories)
    update_act_list()
    update_progress_info()

act_add_button = Button(act_frame, text='Add activity and Update list', command=add_act_command)
act_info_label = Label(act_frame, text='')
act_list = Listbox(act_frame, width=90, height=15, selectmode='single')

act_name_label    .grid(row=0, column=0)
act_name_entry    .grid(row=0, column=1)
act_calories_label.grid(row=1, column=0)
act_calories_entry.grid(row=1, column=1)
act_add_button    .grid(row=2, column=0, columnspan=2)
act_info_label    .grid(row=3, column=0, columnspan=2)
act_list          .place(y=100, x=5)

# - - - profile settings - - - - - - - - - - - - - - - - - - - - - - - -
profile_frame = Frame(tab_switch)

profile_email_label = Label(profile_frame, text='')

def update_user_settings_displays():
    global current_email
    profile_email_label.config(text=f'Email: {current_email}')

    *_, sex, age, weight, height, goal = DBHandler.get_user_info(current_email)
    profile_sex_entry   .set(sex)
    profile_age_entry   .insert(0, age)
    profile_weight_entry.insert(0, weight)
    profile_height_entry.insert(0, height)
    profile_goal_entry  .set(goal)

def update_user_settings():
    if not messagebox.askyesnocancel('Warning: Data Reset', 'Updating user settings requires data reset! Click "YES" to reset progress, meals, and activities.'):
        return

    sex = profile_sex_entry.get()
    age = profile_age_entry.get()
    weight = profile_weight_entry.get()
    height = profile_height_entry.get()
    goal = profile_goal_entry.get()

    try: age = int(age)
    except:     profile_info_label.config(text='Age should be a positive integer', fg='red'); return
    if age < 0: profile_info_label.config(text='Age should be a positive integer', fg='red'); return

    try: weight = int(weight)
    except:        profile_info_label.config(text='Weight should be a positive integer', fg='red'); return
    if weight < 0: profile_info_label.config(text='Weight should be a positive integer', fg='red'); return

    try: height = int(height)
    except:        profile_info_label.config(text='Height should be a positive integer', fg='red'); return
    if height < 0: profile_info_label.config(text='Height should be a positive integer', fg='red'); return

    update_meal_list()
    update_act_list()
    update_user_settings_displays()
    update_progress_info()

    global current_email
    DBHandler.delete_user_data(current_email)
    DBHandler.update_user_info(current_email, sex, age, weight, height, goal)
    profile_info_label.config(text='Your information was changed successfully', fg='green')

profile_sex_label = Label(profile_frame, text='Sex:')
profile_sex_entry = Combobox(profile_frame, state='readonly', values=sex_values)

profile_age_label = Label(profile_frame, text='Age:')
profile_age_entry = Entry(profile_frame)

profile_weight_label = Label(profile_frame, text='Weight:')
profile_weight_entry = Entry(profile_frame)

profile_height_label = Label(profile_frame, text='Height:')
profile_height_entry = Entry(profile_frame)

profile_goal_label = Label(profile_frame, text='Your goal:')
profile_goal_entry = Combobox(profile_frame, state='readonly', values=goal_values)

update_settings_button = Button(profile_frame, text='Update', command=update_user_settings)

def delete_user_data():
    if not messagebox.askyesnocancel('Warning: Data Deletion', 'Clicking "YES" will delete all your data: progress, meals, and activities!'):
        return

    global current_email
    DBHandler.delete_user_data(current_email)
    update_progress_info()

delete_user_data_button = Button(profile_frame, text='Delete all user data', command=delete_user_data)
profile_info_label = Label(profile_frame, text='')

profile_email_label    .grid(row=0, column=0, columnspan=2)
profile_sex_label      .grid(row=1, column=0)
profile_sex_entry      .grid(row=1, column=1)
profile_age_label      .grid(row=2, column=0)
profile_age_entry      .grid(row=2, column=1)
profile_weight_label   .grid(row=3, column=0)
profile_weight_entry   .grid(row=3, column=1)
profile_height_label   .grid(row=4, column=0)
profile_height_entry   .grid(row=4, column=1)
profile_goal_label     .grid(row=5, column=0)
profile_goal_entry     .grid(row=5, column=1)
update_settings_button .grid(row=6, column=0, columnspan=2)
delete_user_data_button.grid(row=7, column=0, columnspan=2)
profile_info_label     .grid(row=8, column=0, columnspan=2)

# - - - miscellaneous settings - - - - - - - - - - - - - - - - - - - - - - - -
tab_switch.add(log_in_frame,  text='Log in')
tab_switch.add(sign_up_frame, text='Sign up')

tab_switch.pack(expand=1, fill='both')

root.title('Calories Diary')
root.geometry('600x400')
root.mainloop()
