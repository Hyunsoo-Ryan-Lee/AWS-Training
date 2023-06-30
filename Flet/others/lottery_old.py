import flet as ft
import mysql.connector
import random

mydb = mysql.connector.connect(
        host="localhost",
        user="hyunsoo",
        password="150808",
        database="flet"
        )

cursor = mydb.cursor()
lottery_number = [str(i).zfill(2) for i  in range(1,46)]

def main(page: ft.Page):
    page.title = "Basic text buttons"
    page.bgcolor = 'WHITE'
    
    def snackBar(msg, color):
        page.snack_bar = ft.SnackBar(
                ft.Text(msg, size=17),
                bgcolor=color,
                duration=2000
                )
        page.snack_bar.open = True
        page.update()
    
    def loaddata(e):
        cursor.execute("SELECT * FROM lotto")
        result = cursor.fetchall()
        numbs = [str(i[1]) for i in result]
        vals = '\n'.join(numbs)
        memo.value = vals
        page.update()

    def deleteall(e):
        cursor.execute("DELETE FROM lotto")
        mydb.commit()
        memo.value = ""
        snackBar("ALL DATA DELETED", 'red')
        page.update()

    def addtodb(e):
        if len(number_text.value) == 6:
            try:
                sql = f"INSERT INTO lotto (day) VALUES({number_text.value})"
                cursor.execute(sql)
                mydb.commit()
                
                cursor.execute("SELECT * FROM lotto")
                result = cursor.fetchall()
                numbs = [str(i[1]) for i in result]
                vals = '\n'.join(numbs)
                memo.value = vals
                # page.update()

                # AND SHOW SNACBAR

                # page.snack_bar = ft.SnackBar(
                #         ft.Text("DAY ADDED",size=17),
                #         bgcolor="green",
                #         duration=2000
                #         )
                # page.snack_bar.open = True
                snackBar("DAY ADDED", 'green')
            except Exception as e:
                print(e)
                print("error you CODE !!!!")
        else:
            snackBar("Please put 6 digit number", 'red')

        number_text.value = ""
        page.update()
        
    def lotto_create(e):
        numb_list = []
        final_number = []
        mod_numb_set = []
        cursor.execute("SELECT * FROM lotto")
        result = cursor.fetchall()
        numbs = [str(i[1]) for i in result]
        for n in numbs:
            numb_list += [n[i*2:i*2+2] for i in range(len(n)//2)]
            numb_list += [n[::-1][i*2:i*2+2] for i in range(len(n)//2)]
        numb_set = list(set(numb_list))
        for i in range(len(numb_set)):
            number = int(numb_set[i])
            if 45 <= number <= 90:
                number -= 45
            elif number > 90:
                number -= 90
            numb_set[i] = str(number).zfill(2)
        numb_set = list(set(numb_set))
        extra_set = [i for i in lottery_number if i not in numb_set]

        if len(numb_set) < 8:
            snackBar("데이터가 부족합니다. 기념일을 더 넣어주세요", 'red')
        else:
            cnt = 0
            if len(numb_set) < 10:
                added_set = random.sample(extra_set, len(numb_set)//2)
            else: added_set = []
            
            try: 
                lotto_cnt = int(cnt_text.value)
                if lotto_cnt <= 0:
                    snackBar("1 이상의 숫자만 입력해주세요", 'red')
                else:
                    while cnt < lotto_cnt:
                        num = random.sample(numb_set+added_set, 6)
                        sorted_num = sorted(num, key=lambda x: int(x))
                        if sorted_num not in final_number:
                            fin = '  '.join(sorted_num)
                            final_number.append(fin)
                            cnt += 1
                        else:
                            pass
                        
                    final_vals = '\n'.join(final_number)
                    lotto_memo.value = final_vals
                    page.update()
            except Exception as e:
                print(e)
                snackBar("숫자만 입력해주세요", 'red')
        
    number_text = ft.TextField(label="기념일(yymmdd)", keyboard_type='NUMBER', color='BLACK', width=300)
    cnt_text = ft.TextField(label="게임 개수", keyboard_type='NUMBER', color='BLACK', width=100)
    btn1 = ft.TextButton(text="입력", on_click=addtodb)
    btn2 = ft.TextButton(text="날짜 조회", on_click=loaddata)
    delete_bnt = ft.FloatingActionButton(text="DATA 삭제", on_click=deleteall, width=100, bgcolor=ft.colors.RED_200)
    load_bnt = ft.ElevatedButton(text="로또 번호 생성", on_click=lotto_create)
    btn_container1 = ft.Container(content=load_bnt, padding=5)
    memo = ft.TextField(label="입력한 기념일", multiline=True, color='BLACK', width=300)
    lotto_memo = ft.TextField(label="추천 번호", multiline=True, color='BLACK', width=300)
    page.add(
        number_text
        , ft.Row(controls=[btn1, btn2])
        , memo
        , ft.Row(controls=[cnt_text, btn_container1])
        , delete_bnt
        , lotto_memo
    )


ft.app(target=main
       , view=ft.WEB_BROWSER
       )