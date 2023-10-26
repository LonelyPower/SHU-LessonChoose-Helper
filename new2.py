# coding: GBK
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import os

def chooselesson(username,password,driver,lesson_id,teacher_id,mode):

    username1 = driver.find_element(By.ID, 'username')
    username1.send_keys(username)
    password1 = driver.find_element(By.ID, 'password')
    password1.send_keys(password)

    element = driver.find_element(By.ID, 'submit-button')
    element.click()

    tr = driver.find_element(By.TAG_NAME, 'tr')
    tr.click()
    button= driver.find_element(By.TAG_NAME, 'button')
    button.click()
    time.sleep(2)
    if mode!='0':
        while(1):
            current_time = time.strftime("%H%M", time.localtime())
            print("当前时间"+current_time+" 目标时间"+mode)
            if current_time == mode:
                break
        
    driver.refresh()
    driver.get('http://xk.autoisp.shu.edu.cn/CourseSelectionStudent/FuzzyQuery')
    time.sleep(20)
    element = driver.find_element(By.NAME, 'CID')
    element.send_keys(lesson_id)
    element = driver.find_element(By.NAME, 'TeachNo')
    element.send_keys(teacher_id)
    
    if mode!='0':
            element = driver.find_element(By.ID, 'QueryAction')
            element.click() 
            element = driver.find_element(By.NAME, 'checkclass')
            element.click()    
            element = driver.find_element(By.ID, 'CourseCheckAction')
            element.click()   
            print('选课成功')
    else:      
        times=0
        while(1):
            
            element = driver.find_element(By.ID, 'QueryAction')
            element.click()        
            # time.sleep(20)
            element = driver.find_element(By.CLASS_NAME, 'red')
            # time.sleep(20)
            if element.text == '人数已满':
                time.sleep(1)
                times+=1
                print('人数已满，第{}次尝试'.format(times))
                continue
            else:
                element = driver.find_element(By.NAME, 'checkclass')
                element.click()    
                element = driver.find_element(By.ID, 'CourseCheckAction')
                element.click()    

                print('选课成功')
                break

def save_data_to_txt(username, password, lesson_id, teacher_id, mode):
    with open('user_data.txt', 'w') as file:
        file.write(f"Username: {username}\n")
        file.write(f"Password: {password}\n")
        file.write(f"Lesson ID: {lesson_id}\n")
        file.write(f"Teacher ID: {teacher_id}\n")
        file.write(f"Mode: {mode}\n")

def load_data_from_txt():
    try:
        with open('user_data.txt', 'r') as file:
            data = file.readlines()
            username = data[0].split(': ')[1].strip()
            password = data[1].split(': ')[1].strip()
            lesson_id = data[2].split(': ')[1].strip()
            teacher_id = data[3].split(': ')[1].strip()
            mode = data[4].split(': ')[1].strip()
            return username, password, lesson_id, teacher_id, mode
    except FileNotFoundError:
        print("未找到用户数据文件")
        return None, None, None, None, None


if os.path.exists('user_data.txt'):
    load_option = input("检测到存在用户数据文件 'user_data.txt', 输入1加载数据，0重新输入 ")
    if load_option.lower() == '1':
        username, password, lesson_id, teacher_id, mode = load_data_from_txt()
        if username is not None:
            print(f"从文件加载的数据：\n学号: {username}\n密码: {password}\n课程号: {lesson_id}\n教师号: {teacher_id}\n模式: {mode}")
    else:
        username=input("请输入学号")
        password=input("请输入密码")    
        lesson_id=input("请输入课程号")
        teacher_id=input("请输入教师号")
        mode=input("如果第三轮蹲点抢课，请输入开始时间，例如八点输入0800、八点半输入 0830，否则输入0")
        flag=input("是否保存用户数据？输入1保存，0不保存") 
        if flag=='1':
            save_data_to_txt(username, password, lesson_id, teacher_id, mode)
            print("数据已保存到文件 'user_data.txt'")
else:
    username=input("请输入学号")
    password=input("请输入密码")    
    lesson_id=input("请输入课程号")
    teacher_id=input("请输入教师号")
    mode=input("如果第三轮蹲点抢课，请输入开始时间，例如八点输入0800、八点半输入 0830，否则输入0")
    
    flag=input("是否保存用户数据？输入1保存，0不保存") 
    if flag=='1':
        save_data_to_txt(username, password, lesson_id, teacher_id, mode)
        print("数据已保存到文件 'user_data.txt'")


driver = webdriver.Edge()
driver.get('http://xk.autoisp.shu.edu.cn')
chooselesson(username,password,driver,lesson_id,teacher_id,mode)
