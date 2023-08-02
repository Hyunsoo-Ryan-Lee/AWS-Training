from flet import *
import mysql.connector

# CONECTION TO DB
lottoDB = mysql.connector.connect(
        host="localhost",
        user="hyunsoo",
        password="910506",
        database="db"
        )

cursor = lottoDB.cursor()


def main(page:Page):
        nametxt = TextField(label="name")
        agetxt = TextField(label="age")


        # CREATE EDIT INPUT
        edit_nametxt = TextField(label="name")
        edit_agetxt = TextField(label="age")
        edit_id = Text()


        mydt = DataTable(
                columns=[
                        DataColumn(Text("id")),
                        DataColumn(Text("name")),
                        DataColumn(Text("age")),
                        DataColumn(Text("actions")),
                ],
                rows=[]

                )

        # DELETE FUNCTION
        def deletebtn(e):
                print("you selected id is = ",e.control.data['id'])
                try:
                        sql = "DELETE FROM main WHERE id = %s"
                        val = (e.control.data['id'],)
                        cursor.execute(sql,val)
                        lottoDB.commit()
                        print("you deleted !!!")
                        mydt.rows.clear()
                        load_data()

                        # AND SHOW SNACBAR

                        page.snack_bar = SnackBar(
                                Text("Data success Deleted",size=20),
                                bgcolor="red"

                                )
                        page.snack_bar.open = True
                        page.update()
                except Exception as e:
                        print(e)
                        print("error you code for delete")


        def savedata(e):
                try:
                        sql = "UPDATE main SET age = %s , name = %s WHERE id = %s"
                        val = (edit_agetxt.value,edit_nametxt.value,edit_id.value)
                        cursor.execute(sql,val)
                        lottoDB.commit()
                        print("you succes edit data")
                        dialog.open = False
                        page.update()

                        # CLEAR EDIT TEXTFIELD
                        edit_nametxt.value = ""
                        edit_agetxt.value = ""
                        edit_id.value = ""

                        mydt.rows.clear()
                        load_data()

                        # AND SHOW SNACBAR

                        page.snack_bar = SnackBar(
                                Text("Data success EDIT",size=20),
                                bgcolor="green"

                                )
                        page.snack_bar.open = True
                        page.update()
                except Exception as e:
                        print(e)
                        print("ERROR SAVE EDIT !!!")

        # CREATE DIALOG SHOW WHEN YOU CLICK EDIT BUTTON
        dialog = AlertDialog(
                title=Text("Edit data"),
                content=Column([
                        edit_nametxt,
                        edit_agetxt

                        ]),
                actions=[
                        TextButton("Save",
                                on_click=savedata
                                )

                ]

                )


        # EDIT FUNCTION
        def editbtn(e):
                edit_nametxt.value = e.control.data['name']
                edit_agetxt.value = e.control.data['age']
                edit_id.value = e.control.data['id']

                page.dialog = dialog
                dialog.open = True
                page.update()



        def load_data():
                # GET ALL DATA FROM DATABASE AND PUSH TO DATATABLE
                cursor.execute("SELECT * FROM main")
                result = cursor.fetchall()

                # AND PUSH DATA TO DICT
                columns = [column[0] for column in cursor.description]
                rows = [dict(zip(columns,row)) for row in result]


                # LOOP AND PUSH
                for row in rows:
                        mydt.rows.append(
                                DataRow(
                                        cells=[
                                                DataCell(Text(row['id'])),
                                                DataCell(Text(row['name'])),
                                                DataCell(Text(row['age'])),
                                                DataCell(
                                                        Row([
                                                        IconButton("delete",icon_color="red",
                                                                data=row,
                                                                on_click=deletebtn
                                                                ),
                                                        IconButton("create",icon_color="red",
                                                                data=row,
                                                                on_click=editbtn
                                                                ),


                                                                ])
                                                        ),

                                        ]

                                        )

                                )
                page.update()


        # AND CALL FUNCTION WHEN YOU APP IS FIRST OPEN
        load_data()

        def addtodb(e):
                try:
                        sql = "INSERT INTO main (name,age) VALUES(%s,%s)"
                        val = (nametxt.value,agetxt.value)
                        cursor.execute(sql,val)
                        lottoDB.commit()
                        print(cursor.rowcount,"YOU RECORD INSERT !!!")

                        # AND CLEAR ROWS IN TABLE AND PUSH FROM DATABASE AGAIN
                        mydt.rows.clear()
                        load_data()

                        # AND SHOW SNACBAR

                        page.snack_bar = SnackBar(
                                Text("Data success add",size=20),
                                bgcolor="green"

                                )
                        page.snack_bar.open = True
                        page.update()
                except Exception as e:
                        print(e)
                        print("error you CODE !!!!")

                # AND AFTER YOU SUCCESS INPUT TO DB THEN CLEAR TEXTINPUT
                nametxt.value = ""
                agetxt.value = ""
                page.update()

        page.add(
        Column([
                nametxt,
                agetxt,
                ElevatedButton("ADD",
                        on_click=addtodb
                        ),
                mydt

                ])

                )
    
app(port = 3456
       , target=main
       , view=WEB_BROWSER
       )


# create table main(id int(11) NOT NULL AUTO_INCREMENT, name varchar(30) NOT NULL, age int(11) NOT NULL, PRIMARY KEY (id));