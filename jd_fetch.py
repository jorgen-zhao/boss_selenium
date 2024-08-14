#encoding='utf-8'
from selenium import webdriver
import time
import random
from selenium.webdriver.common.by import By
import pandas as pd
import os
from selenium.webdriver import Keys, ActionChains,ChromeOptions
from datetime import datetime

def close_windows():
    #如果有登录弹窗，就关闭
    try:
        dr.implicitly_wait(20)#智能等待20秒，等待页面的元素加载出来后，就继续执行，下同
        if dr.find_element(By.XPATH,'//div[@class="boss-login-dialog"]//i[@class="icon-close"]'):
            dr.find_element(By.XPATH,'//div[@class="boss-login-dialog"]//i[@class="icon-close"]').click()
            #13 14行代码的作用是判断是否有弹出登录框，如果弹出登录框则右上角的关闭按钮，若无则跳过执行并告知没有弹窗
    except:
        print('close_windows,没有弹窗')

columns=['岗位名称', '行业类型', '融资情况', '企业规模', '企业福利', '薪资范围', '工作年限', '学历要求', 
             '岗位关键字', '岗位职责', 'boss名称', '活跃时间', 'boss简介', '公司简介', '公司名称',"法人", "成立日期", "公司类型", 
             "经营状态", "注册资金", "公司地址"]
df = pd.DataFrame(columns=columns)
def get_current_region_job(query, city_no):
    file_name = query+ "_" + city_no+ "_" + datetime.now().strftime("%Y%m%d%H%M%S")
    global df  # 如果 df 是在函数外部定义的，确保在此处声明为全局变量
    #该函数的作用是获取指定城市指定区域的岗位信息
    flag = 0
    global dr
    # 创建Chrome参数对象
    options = webdriver.ChromeOptions()
    # 添加试验性参数
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    
    # options = ChromeOptions()
    # options.add_argument("--headless=new")  
    dr = webdriver.Chrome()
    # 创建Chrome浏览器对象并传入参数
    dr.execute_cdp_cmd(
        'Page.addScriptToEvaluateOnNewDocument',
        {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'}
    )
    # 初始化webdriver
    # 读取文件
    with open('stealth.min.js', 'r') as f:
        js = f.read()
    # 调用函数在页面加载前执行脚本
    dr.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': js})
    
    # 转到目标网址
    dr.get("https://www.zhipin.com/web/geek/job?query={0}&city={1}&experience=106&scale=303,304,305,306&page=3".format(query, city_no))  # sz
    print("打开网址")
    time.sleep(random.randint(3, 5))
    count = 0
    while (flag == 0):
        dr.implicitly_wait(5)
        time.sleep(random.randint(3, 5))
        job_detail = dr.find_elements(By.XPATH,'//ul[@class="job-list-box"]/li')#这里是获取所有的岗位信息块
        print("get job list")
        
        for job in job_detail:
        # 岗位名称
            try:
                dr.implicitly_wait(5)
                job_title = job.find_element(By.CSS_SELECTOR, '.job-name').text#获取岗位名称
                print("job_title.....", job_title)
            except:
                print("excepting job title.....")
                continue
            # 行业类型
            dr.implicitly_wait(5)
            job_industry = job.find_elements(by=By.CSS_SELECTOR, value=".company-tag-list")[0].text
            job_finance = job.find_elements(by=By.CSS_SELECTOR, value=".company-tag-list")[0].text
            
            try:
                # 企业规模
                job_scale = job.find_element(by=By.XPATH, value="./div[1]/div/div[2]/ul/li[3]").text.strip()
            except:
                job_scale = "无"
            try:
                # 企业福利
                job_welfare = job.find_element(by=By.XPATH, value="./div[2]/div").text.strip()
            except:
                job_welfare = '无'
            try:
                # 薪资范围
                job_salary_range = job.find_element(By.CSS_SELECTOR, '.salary').text  # 获取薪资
            except:
                job_salary_range = "无"
            # 工作年限
            try:
                job_experience = job.find_element(by=By.XPATH, value="./div[1]/a/div[2]/ul/li[1]").text.strip()
            except:
                job_experience = "无"
            # 学历要求
            try:
                job_education = job.find_element(by=By.XPATH, value="./div[1]/a/div[2]/ul/li[2]").text.strip()
            except:
                job_education = "无"
            
            original_window_handles = dr.window_handles
            print("original_window_handles:" , original_window_handles)
            if (job_title):
                element = job.find_element(by=By.XPATH, value="./div[1]/a/div[1]/span[1]")
                dr.execute_script("arguments[0].click();", element)
            print("打开详情页")
            
            
            dr.switch_to.window(dr.window_handles[1])
            original_window_handles = dr.window_handles
            print("after click window_handles:" , original_window_handles)

            time.sleep(random.randint(3, 5))
            close_windows()
            dr.implicitly_wait(5)
            # 工作地址
            try:
                job_keywords = ','.join(
                    [skill.text.strip() for skill in dr.find_elements(by=By.CSS_SELECTOR, value=".job-keyword-list")])
            except:
                job_keywords = '无'
            if (job_salary_range == "无"):
                try:
                    job_salary_range = job.find_element(By.CSS_SELECTOR, '.salary').text  # 获取薪资
                except:
                    job_salary_range = "无"
            
            if (job_experience == "无"):
                try:
                    job_experience = job.find_element(by=By.CSS_SELECTOR, value=".text-desc text-experiece").text.strip()
                except:
                    job_experience = "无"
            if (job_education == "无"):
                try:
                    job_education = job.find_element(by=By.CSS_SELECTOR, value=".text-desc text-degree").text.strip()
                except:
                    job_education = "无"

            for i in range(random.randint(3, 8)):
                ActionChains(dr).send_keys(Keys.ARROW_DOWN).perform()

            try:
                job_detail = dr.find_element(By.CSS_SELECTOR, ".job-sec-text:nth-child(4)").text.strip()
            except:
                job_detail = "无"

            try:
                boss_name = dr.find_element(By.CSS_SELECTOR, ".job-boss-info > .name").text.strip()
            except:
                boss_name = "无"

            try:
                boss_active_time = dr.find_element(By.CSS_SELECTOR, ".boss-active-time").text.strip()
            except:
                boss_active_time = "无"

            try:
                boss_info = dr.find_element(By.CSS_SELECTOR, ".boss-info-attr").text.strip()
            except:
                boss_info = "无"

            try:
                company_info = dr.find_element(By.CSS_SELECTOR, ".fold-text").text.strip()
            except:
                company_info = "无"

            try:
                company_full_name = dr.find_element(By.CSS_SELECTOR, ".company-name:nth-child(1)").text.strip()
            except:
                company_full_name = "无"

            try:
                company_user = dr.find_element(By.CSS_SELECTOR, ".company-user").text.strip()
            except:
                company_user = "无"

            try:
                res_time = dr.find_element(By.CSS_SELECTOR, ".res-time").text.strip()
            except:
                res_time = "无"

            try:
                company_type = dr.find_element(By.CSS_SELECTOR, ".company-type").text.strip()
            except:
                company_type = "无"

            try:
                manage_state = dr.find_element(By.CSS_SELECTOR, ".manage-state").text.strip()
            except:
                manage_state = "无"

            try:
                company_fund = dr.find_element(By.CSS_SELECTOR, ".company-fund").text.strip()
            except:
                company_fund = "无"

            try:
                location_address = dr.find_element(By.CSS_SELECTOR, ".location-address").text.strip()
            except:
                location_address = "无"

            data_row = {
                '岗位名称': job_title, 
                '行业类型':job_industry, 
                '融资情况': job_finance, 
                '企业规模':job_scale, 
                '企业福利': job_welfare, 
                '薪资范围':job_salary_range, 
                '工作年限':job_experience, 
                '学历要求':job_education, 
                '岗位关键字': job_keywords,
                '岗位职责': job_detail,
                'boss名称': boss_name,
                '活跃时间': boss_active_time,
                'boss简介': boss_info,
                '公司简介': company_info,
                '公司名称': company_full_name,
                "法人": company_user,
                "成立日期": res_time,
                "公司类型": company_type,
                "经营状态": manage_state,
                "注册资金": company_fund,
                "公司地址": location_address,
                }

            # 关闭详情页
            dr.close()
            dr.switch_to.window(dr.window_handles[0])
            
            original_window_handles = dr.window_handles
            print("closed original_window_handles:" , original_window_handles)
            dfee = df.append(data_row, ignore_index=True)
            mode = 'a' if os.path.exists(file_name+".csv") else 'w'
            dfee.to_csv(file_name+'.csv', mode=mode, header=mode=='w', index=False, encoding='utf-8-sig')
            count = count + 1
            print("已经读取数据{}条".format(count))

            time.sleep(random.randint(2, 5))

        #点击下一页
        try:
            dr.implicitly_wait(20)
            cur_page_num=dr.find_element(By.XPATH,'//div[@class="options-pages"]//a[@class="selected"]').text#当前所在页面的按钮上的数字
            print('cur_page_num:',cur_page_num)
            #点击下一页
            dr.implicitly_wait(20)
            element = dr.find_element(By.XPATH,'//i[@class="ui-icon-arrow-right"]')#找到点击下一页的按钮
            dr.implicitly_wait(20)
            dr.execute_script("arguments[0].click();", element)
            dr.implicitly_wait(20)
            new_page_num=dr.find_element(By.XPATH,'//div[@class="options-pages"]//a[@class="selected"]').text#点击下一页按钮后，当前所在页面的按钮上的数字
            print('new_page_num',new_page_num)
            if cur_page_num==new_page_num:#如果当前页面与最新页面的数字一致，则表示已经是最后一页，跳出循环
                flag = 1
                break
           
        except BaseException as e:
            print('点击下一页错误',e)
            break

if __name__ == '__main__':
    program_start_time = time.time()  # 记录开始时间
    get_current_region_job('Java 物联网','101280600')#北京
    program_end_time = time.time()  # 记录开始时间
    elapsed_time = program_end_time - program_start_time  
    print(f"程序总耗时：{elapsed_time}秒")
