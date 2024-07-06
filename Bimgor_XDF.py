from config import put, put_plenki
import customtkinter as cst
from time import strftime
import shutil
import os

cst.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
cst.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(cst.CTk):
    def __init__(self):
        super().__init__()
        self.title("Bimgor")
        self.resizable(False, False)

        def center_window(width=565, height=430):
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            x = (screen_width / 2) - (width / 2)
            y = (screen_height / 2) - (height / 2)
            self.geometry('%dx%d+%d+%d' % (width, height, x, y))

        def serd_nomer(zakaz):
            btn_15.place_forget()
            self.text_box.configure(font=self.font_1)
            shutil.copyfile(put + self.op_god.get()[-2:] + '.RSB', '23.txt')
            for i in open(u'23.txt'):
                if i[108:112] == zakaz and (not i[112].isdigit()):
                    self.text_box.delete("0.0", cst.END)
                    return self.text_box.insert("0.0", 'Наш номер заказа ' + i[:4])
            self.text_box.configure(font=self.font_1)
            self.text_box.delete("0.0", cst.END)
            return self.text_box.insert("0.0", 'Нету')

        def plenki(num):
            btn_15.place_forget()
            self.text_box.configure(font=self.font_1)
            b = []
            a = open(put_plenki, 'r+').readlines()
            for line in range(len(a)):
                if a[line] == "' ПЛЕНКА\n":
                    for i in range(line + 1, len(a)):
                        s = a[i].split('|')[:3]
                        if s[0] == '!\n':
                            break
                        b.append(s)
            for x in b:
                if x[0] == num:
                    self.text_box.delete("0.0", cst.END)
                    return self.text_box.insert("0.0", f'{x[1]}\n            группа {x[2]}')
                    break
            self.text_box.delete("0.0", cst.END)
            return self.text_box.insert("0.0", f'нет такого номера')

        def xdf_fasad(zakaz):
            btn_15.configure(text='Печать', command=lambda: os.startfile('Bimgor_XDF.txt'))
            btn_15.place(x=410, y=305)
            self.text_box.configure(font=self.font_1)
            shutil.copyfile(put + self.op_god.get()[-2:] + '.RSB', '23.txt')
            f = open(u'23.txt').read().split('#@#')
            k, s, kof_PS, kof_BUT = f'+{"-" * 15}+\n| Заказ №  {self.entry_4.get()} |\n+{"-" * 15}+\n', [], 0, 0
            fas = [[96, 97, 103, 107, 108, 110, 113, 117], [98], [100]]
            steklo = ['', 'Планка', 'СТЕКЛО', 'Бленда1', 'Бленда2', 'Бленда3', 'Бленда4', 'ПЕРЕПЛЕТ']
            for i in f:
                if i[1:5] == zakaz:
                    kv_m = 0
                    for j in i.split('\n')[3:-1]:
                        s = j.split('|')[:11]
                        if not s[5].isdigit() or s[7] in steklo:
                            continue
                        elif int(s[5]) in fas[0]:
                            if int(s[1]) < 133 or int(s[2]) < 133:
                                continue
                            if self.entry_4_2.get() == '':
                                kof_PS = kof_BUT = 130
                            else:
                                kof_PS = kof_BUT = int(self.entry_4_2.get())
                            if s[7] == 'ПСЯ': kof_PS = kof_PS - 44
                            if s[7] == 'Бутыл.': kof_BUT = kof_BUT - 44
                            kv_m += float(s[10])
                        elif int(s[5]) in fas[1]:
                            if int(s[1]) < 133 or int(s[2]) < 133:
                                continue
                            if self.entry_4_2.get() == '':
                                kof_PS = kof_BUT = 144
                            else:
                                kof_PS = kof_BUT = int(self.entry_4_2.get())
                            if s[7] == 'ПСЯ': kof_PS = 86
                            if s[7] == 'Бутыл.': kof_BUT = 86
                            kv_m += float(s[10])
                        elif int(s[5]) in fas[2]:
                            if self.entry_4_2.get() == '':
                                kof_PS = kof_BUT = 45
                            else:
                                kof_PS = kof_BUT = int(self.entry_4_2.get())
                            kv_m += float(s[10])
                        else:
                            continue
                        s[1] = str(int(s[1]) - kof_PS)
                        s[2] = str(int(s[2]) - kof_BUT)
                        k += f'|{s[0]:>2}|{s[1]:>4}|{s[2]:>4}|{s[3]:>2}|\n'
                    k += f'+{"-" * 15}+\n| Всего {kv_m:.2f} m{chr(178)} |\n+{"-" * 15}+'
            with open("Bimgor_XDF.txt", "w", encoding="utf-16") as file:
                file.writelines(k)

            self.text_box.delete("0.0", cst.END)
            return self.text_box.insert("0.0", k)

        def zarplata():
            btn_15.configure(text='Подробно', command=lambda: os.startfile('zarplata.txt'))
            btn_15.place(x=410, y=305)
            shutil.copyfile(put + self.op_god.get()[-2:] + '.RSB', '23.txt')
            count, metraj, spisok, srochno = 1, 0.0, '', ''
            col_Rost, col_R16 = 0, 0
            P, R = [0.0] * 10, [0.0] * 4
            if self.op_menu.get() in ('Январь', 'Февраль', 'Март', 'Апрель'):
                shutil.copyfile(put + str(int(self.op_god.get()[-2:]) - 1) + '.RSB', '22.txt')
                b = open(u'22.txt', 'r+').read()
                a = open(u'23.txt', 'a').write(b)
            a = open(u'23.txt', 'r+').readlines()
            for line in range(len(a) - 2):
                B, A, C = a[line].split('|'), a[line + 1].split('|'), a[line + 2].split('|'),
                if len(B[0]) == 4 and B[0].isdigit() and B[14] == self.mesyac.get(self.op_menu.get()) \
                        and B[5][:2] == self.op_god.get()[2:] and B[12] == '  .  ':
                    st_dart = ["Агаджанов", "Ростов", "Сорокин", "Миша Москва", "Кузнецов С"]
                    if len(C[9]) > 3 and B[1].strip() in st_dart and C[9][3] == "`":
                        A[0] = "I  -  16 не ст-т"

                    K = [0.0] * 6
                    if A[0][9:11] == 'не':
                        P[0] += float(A[12])
                        K[0] += float(A[12])
                    elif A[0][9:11] == 'ст':
                        P[1] += float(A[12])
                        K[1] += float(A[12])
                    elif A[0][9:11] == 'АР':
                        P[2] += float(A[12])
                        K[2] += float(A[12])
                    elif A[0][4:6] == 'Фр':
                        P[4] += float(A[12])
                        K[4] += float(A[12])

                    if A[1][9:11] == 'не':
                        P[0] += float(A[13])
                        K[0] += float(A[13])
                    elif A[1][9:11] == 'ст':
                        P[1] += float(A[13])
                        K[1] += float(A[13])
                    elif A[1][9:11] == 'АР':
                        P[2] += float(A[13])
                        K[2] += float(A[13])
                    elif A[1][4:6] == 'Фр':
                        P[4] += float(A[13])
                        K[4] += float(A[13])

                    if A[2][9:11] == 'не':
                        P[0] += float(A[14])
                        K[0] += float(A[14])
                    elif A[2][9:11] == 'ст':
                        P[1] += float(A[14])
                        K[1] += float(A[14])
                    elif A[2][9:11] == 'АР':
                        P[2] += float(A[14])
                        K[2] += float(A[14])
                    elif A[2][4:6] == 'Фр':
                        P[4] += float(A[14])
                        K[4] += float(A[14])

                    if A[3][9:11] == 'не':
                        P[0] += float(A[15])
                        K[0] += float(A[15])
                    elif A[3][9:11] == 'ст':
                        P[1] += float(A[15])
                        K[1] += float(A[15])
                    elif A[3][9:11] == 'АР':
                        P[2] += float(A[15])
                        K[2] += float(A[15])
                    elif A[3][4:6] == 'Фр':
                        P[4] += float(A[15])
                        K[4] += float(A[15])

                    if A[4][9:11] == 'не':
                        P[0] += float(A[16])
                        K[0] += float(A[16])
                    elif A[4][9:11] == 'ст':
                        P[1] += float(A[16])
                        K[1] += float(A[16])
                    elif A[4][9:11] == 'АР':
                        P[2] += float(A[16])
                        K[2] += float(A[16])
                    elif A[4][4:6] == 'Фр':
                        P[4] += float(A[16])
                        K[4] += float(A[16])

                    K[5] = K[0] + K[1] + K[2] + K[3] + K[4]
                    if B[26] != '':
                        P[6] += float(B[26])

                    # Закатка
                    if A[0][4:6] == "За":
                        P[5] += float(A[12])

                    # радиус
                    if A[19] != ' 0':
                        for i in range(line, line + 50):
                            D = a[i].split('|')
                            if D[0][:3] == '#@#':
                                break
                            if len(D[5]) > 0 and D[5][0] == 'R' and D[5][1:3] != '16' and D[5] != 'RКАРНИЗ':
                                col_Rost += int(D[3])
                            if D[5] == 'R16':
                                col_R16 += int(D[3])

                    # срочно
                    if A[28] != '':
                        if A[28] == '1000.00': A[28] = '1000'
                        P[3] += float(A[28])
                        srochno += '{}|{}|{}|{}{}\n'.format(str(count).rjust(4, '_'), B[0], B[1].replace(' ', '_'),
                                                            '__срочность_____', str(A[28]).strip(), '__руб.')

                    spisok += '{}|{}|{}|{}|{}|{}|{}|{}|{}|\n'.format(str(count).rjust(4, '_'), B[0],
                                                                     B[1].replace(' ', '_'),
                                                                     B[23].rjust(7, '_'),
                                                                     str(round(K[1], 2)).rjust(7, '_'),
                                                                     str(round(K[0], 2)).rjust(7, '_'),
                                                                     str(round(K[2], 2)).rjust(7, '_'),
                                                                     str(round(K[4], 2)).rjust(7, '_'),
                                                                     B[26].rjust(7, '_'))

                    count += 1
                    metraj = str(round(P[0] + P[1] + P[2] + P[4] + P[5], 2))
            with open('20.txt', 'r', encoding='UTF-8') as file_2:
                f = file_2.read().replace('2023', self.op_god.get()).replace('Май', self.op_menu.get()) \
                    .replace("МЕТРАЖ_0", "МЕТРАЖ_" + f' {metraj}') \
                    .replace("СТАНДАРТ_____0", "СТАНДАРТ_____" + f' {P[1]:.2f}') \
                    .replace("НЕ_СТАНДАРТ__0", "НЕ_СТАНДАРТ__" + f' {P[0]:.2f}') \
                    .replace("КАРНИЗЫ______0", "КАРНИЗЫ______" + f' {P[2]:.2f}') \
                    .replace("ЗАКАТКА______0", "ЗАКАТКА______" + f' {P[5]:.2f}') \
                    .replace("ФРЕЗЕРОВКА___0", "ФРЕЗЕРОВКА___" + f' {P[4]:.2f}') \
                    .replace("Радиус_мыло__0", "Радиус_мыло__" + f' {col_R16}') \
                    .replace("Радиус_остр._0", "Радиус_остр._" + f' {col_Rost}') \
                    .replace("СРОЧНО_______0", "СРОЧНО_______" + f'{round(P[3]): ,}') \
                    .replace("ОБЩАЯ_СУММА__0", "ОБЩАЯ_СУММА__" + f'{round(P[6]): ,}') \
                    .replace('сумма|', 'сумма|\n' + spisok) \
                    .replace('Заказы', 'Заказы\n' + srochno)

                with open('zarplata.txt', 'w', encoding='UTF-8') as file_3:
                    file_3.write(f)

                with open('zarplata.txt', 'r', encoding='UTF-8') as file_4:
                    self.text_box.delete("0.0", cst.END)
                    self.text_box.configure(font=self.font_3)
                    return self.text_box.insert("0.0", file_4.read(240))

        def serdyuch(zakaz):
            btn_15.place_forget()
            shutil.copyfile(put + self.op_god.get()[-2:] + '.RSB', '23.txt')
            a = open(u'23.txt').readlines()
            k2, j = '', 0
            for i in range(len(a)):
                if a[i][:4] == zakaz:
                    while a[i][:3] != '#@#':
                        s = a[i].replace('/', '|').split('|')
                        if j == 0:
                            k2 += '{}|{}|{}|\nцвет {}|{}|{}|метраж {}|кол. {}|\n'.format \
                                (s[0], s[1].strip(), s[16], s[17], s[18], s[19], s[23], s[24])
                        if j == 1:
                            ch1 = '+' if s[25][1] == '1' else '-'
                            ch2 = '+' if s[25][2] == '1' else '-'
                            ch3 = '+' if s[25][3] == '1' else '-'
                            k2 += '|раскрой{}|фрезер{}|пресс{}|\n{}\n'.format(ch1, ch2, ch3, 35 * "-")
                        if j >= 2:
                            k2 += '{}|{}|{}|{}|{}|{}|{}|{}|{}\n'.format(s[0], s[1], s[2], \
                                                                        s[3], s[5], s[6], s[7], s[8], s[9])
                        i += 1
                        j += 1
                        if i == len(a):
                            break
                    self.text_box.delete("0.0", cst.END)
                    self.text_box.configure(font=self.font_2)
                    return self.text_box.insert("0.0", k2)

        def imya_akaza(zakaz):
            btn_15.place_forget()
            self.text_box.configure(font=self.font_1)
            shutil.copyfile(put + self.op_god.get()[-2:] + '.RSB', '23.txt')
            a = open(u'23.txt', 'r+').readlines()
            for line in range(len(a)):
                S = a[line].split('|')
                if S[0] == zakaz:
                    temp1, temp2 = str(S[1]).rstrip(), self.entry_22.get()
                    S[1] = self.entry_22.get().ljust(18, ' ')
                    a[line] = '|'.join(S)
                    open(u'Bimgor_XDF.txt', 'w', True).writelines(a)
                    shutil.copyfile('Bimgor_XDF.txt', put + self.op_god.get()[-2:] + '.RSB')
                    self.text_box.delete("0.0", cst.END)
                    return self.text_box.insert("0.0", temp1 + ' на ' + temp2)
            self.text_box.delete("0.0", cst.END)
            return self.text_box.insert("0.0", 'Нету')

        def nomer_akaza(zakaz):
            btn_15.place_forget()
            self.text_box.configure(font=self.font_1)
            shutil.copyfile(put + self.op_god.get()[-2:] + '.RSB', '23.txt')
            a = open(u'23.txt', 'r+').readlines()
            for line in range(len(a)):
                S = a[line].split('|')
                if S[0] == zakaz:
                    temp1, temp2 = str(S[0]), self.entry_33.get()
                    S[0] = self.entry_33.get()
                    a[line] = '|'.join(S)
                    open(u'Bimgor_XDF.txt', 'w', True).writelines(a)
                    shutil.copyfile('Bimgor_XDF.txt', put + self.op_god.get()[-2:] + '.RSB')
                    self.text_box.delete("0.0", cst.END)
                    return self.text_box.insert("0.0", temp1 + ' на ' + temp2)
            self.text_box.delete("0.0", cst.END)
            return self.text_box.insert("0.0", 'Нету')

        center_window()
        self.mesyac = {'Январь': '01', 'Февраль': '02', 'Март': '03', 'Апрель': '04',
                       'Май': '05', 'Июнь': '06', 'Июль': '07', 'Август': '08',
                       'Сентябрь': '09', 'Октябрь': '10', 'Ноябрь': '11', 'Декабрь': '12'}

        self.font_1 = ('Consolas', 20, 'bold')
        self.font_2 = ('Consolas', 15, 'bold')
        self.font_3 = ('Consolas', 19, 'bold')

        self.frame_1 = cst.CTkFrame(self, width=150, height=460)
        self.frame_1.place(x=5, y=5)
        self.frame_2 = cst.CTkFrame(self, width=400, height=39)
        self.frame_2.place(x=160, y=5)
        self.frame_3 = cst.CTkFrame(self, width=400, height=36)
        self.frame_3.place(x=160, y=349)
        self.frame_4 = cst.CTkFrame(self, width=400, height=36)
        self.frame_4.place(x=160, y=389)

        self.text_box = cst.CTkTextbox(self.frame_2, width=390, height=329, font=self.font_1)
        self.text_box.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

        self.s = strftime("%Y")
        self.op_god = cst.CTkOptionMenu(self.frame_1, width=140, font=self.font_2,
                                        values=[self.s, str(int(self.s) - 1), str(int(self.s) - 2)])
        self.op_god.pack(pady=(5, 15), padx=5)

        self.btn1 = cst.CTkButton(self.frame_1, text='Сердюченко', width=140,
                                  font=self.font_2, command=lambda: serd_nomer(self.entry_1.get()))
        self.btn1.pack(pady=5, padx=5)
        self.entry_1 = cst.CTkEntry(self.frame_1, width=140, font=self.font_2, placeholder_text="№ Заказа")
        self.entry_1.pack(pady=5, padx=5)

        self.btn6 = cst.CTkButton(self.frame_1, text='Готовность', width=140,
                                  command=lambda: serdyuch(self.entry_1.get()), font=self.font_2)
        self.btn6.pack(pady=5, padx=5)

        self.entry_5 = cst.CTkEntry(self.frame_1, width=140, font=self.font_2, placeholder_text="№ Пленки")
        self.entry_5.pack(pady=(15, 5), padx=5)
        self.btn4 = cst.CTkButton(self.frame_1, text='Наз. плкнки', width=140,
                                  command=lambda: plenki(self.entry_5.get()), font=self.font_2)
        self.btn4.pack(pady=5, padx=5)

        self.entry_4 = cst.CTkEntry(self.frame_1, width=76, font=self.font_2, placeholder_text="№ Заказа")
        self.entry_4.place(x=5, y=260)
        self.entry_4_2 = cst.CTkEntry(self.frame_1, width=57, font=self.font_2)
        self.entry_4_2.place(x=87, y=260)
        self.btn4 = cst.CTkButton(self.frame_1, text='Размер ХДФ', width=140,
                                  command=lambda: xdf_fasad(self.entry_4.get()), font=self.font_2)
        self.btn4.pack(pady=(53, 5), padx=5)

        self.op_menu = cst.CTkOptionMenu(self.frame_1, width=140, font=self.font_2,
                                         values=[key for key in self.mesyac.keys()])
        self.op_menu.pack(pady=(15, 5), padx=5)
        self.op_menu.set(list(self.mesyac.keys())[list(self.mesyac.values()).index(strftime("%m"))])
        self.btn5 = cst.CTkButton(self.frame_1, text='Зарплата', width=140,
                                  command=zarplata, font=self.font_2)
        self.btn5.pack(pady=5, padx=5)

        self.btn2 = cst.CTkButton(self.frame_3, text='Имя Заказа', width=140,
                                  command=lambda: imya_akaza(self.entry_2.get()), font=self.font_2)
        self.btn2.pack(side=cst.LEFT, pady=5, padx=5)

        self.entry_2 = cst.CTkEntry(self.frame_3, width=90, font=self.font_2, placeholder_text="№ Заказа")
        self.entry_2.pack(side=cst.LEFT, pady=5, padx=5)

        self.entry_22 = cst.CTkEntry(self.frame_3, width=140, font=self.font_2, placeholder_text="Фамилия")
        self.entry_22.pack(side=cst.LEFT, pady=5, padx=5)

        self.btn3 = cst.CTkButton(self.frame_4, text='Номер заказа', width=140,
                                  command=lambda: nomer_akaza(self.entry_3.get()), font=self.font_2)
        self.btn3.pack(side=cst.LEFT, pady=5, padx=5)

        self.entry_3 = cst.CTkEntry(self.frame_4, width=90, font=self.font_2, placeholder_text="№ какой")
        self.entry_3.pack(side=cst.LEFT, pady=5, padx=5)

        self.entry_33 = cst.CTkEntry(self.frame_4, width=140, font=self.font_2, placeholder_text="№ на какой")
        self.entry_33.pack(side=cst.LEFT, pady=5, padx=5)

        btn_15 = cst.CTkButton(self, width=140, font=self.font_2, bg_color="grey20",)

        btn_15.place_forget()


def change_appearance_mode_event(self, new_appearance_mode):
    cst.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
