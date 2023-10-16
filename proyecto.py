import flet as ft
from itertools import product
import re

def main(page: ft.Page):
    page.title = "Simulador de Circuitos"
    page.theme_mode = ft.ThemeMode.LIGHT

    alert = ft.AlertDialog(
        title=ft.Text("Valores Erroneos", color="red"),
        content= ft.Text("Los valores ingresados no son válid   os\nUtilizar 0 y 1"),
        content_padding=20
    )

    def mostrarAlerta():
        page.dialog = alert
        alert.open = True
        page.update()
    
   
    def agregarSalida(e):
        salidaStr = list(tb.value)
        salida = []
        for valor in salidaStr:
            if valor != '0' and valor != '1':
                mostrarAlerta()
            salida.append(int(valor))
        return salida
    
    def digitsFormat(x):
        digit = 0
        if x:
            digit = 1
        return digit
    
    mat = []
    def mostrarSalida(e):
        mat.clear()
        salida = agregarSalida(e)
        indice = 0
        lv.controls.append(ft.Text(f"a   b   c   d  |  s"))
        lv.controls.append(ft.Text(f"-----------------"))
        for a, b, c, d in product((True, False), repeat=4):
            lv.controls.append(ft.Text(f"{digitsFormat(a)}   {digitsFormat(b)}   {digitsFormat(c)}   {digitsFormat(d)}  |  {digitsFormat(salida[indice])}"))
            indice += 1
            page.update()
        #Creacion matriz con la salida
    
    def matriz(e):
        salida = agregarSalida(e)
        indice2 = 0
        for a, b, c, d in product((True, False), repeat=4):
            if salida[indice2] == 1:
                mat.append([digitsFormat(a), digitsFormat(b), digitsFormat(c), digitsFormat(d), digitsFormat(salida[indice2])])
            indice2 = indice2 + 1
            page.update()

    
    
    #CIrcuito por miniteminos
    

    def digitToForm(letra, x):
        cadena = ""
        if x == 0:
            cadena += letra.upper()
        else:
            cadena += letra
        return cadena

    def formula(mat):
        n = len(mat)
        stringFormula = ""
        for i in range(0, n):
            for j in range (0, 4):
                if j == 0:
                    letra = 'a'
                elif j == 1:
                    letra = 'b'
                elif j == 2:
                    letra = 'c'
                elif j == 3:
                    letra = 'd'
                stringFormula += digitToForm(letra, mat[i][j])
            if i < n - 1:
                stringFormula += " + "
        return stringFormula

    

    def mostrarFormula(e):
        matriz(e)
        formulaGeneralStr = formula(mat)
        formulaGeneralTxt.value = f"Circuito por miniterminos:\n S = {formulaGeneralStr}"
        page.update()

    #Traduciendo la cadena a valores booleanos
    
    
    def stringToBoolean(sumandos):
        allExpresion = []
        for sumando in sumandos:
            parcial = []
            for factor in sumando:
                if factor.isupper():
                    aux = False
                else:
                    aux = True
                parcial.append(aux)
            allExpresion.append(parcial)
        return allExpresion
    
    # booleanAllExpresion = stringToBoolean(sumandos)
    
    def agregarCodigo(e):
        codigoText = list(codigoTxt.value)
        codigo = []
        for valor in codigoText:
            if valor != '0' and valor != '1':
                mostrarAlerta()
            codigo.append(int(valor))
        return codigo
    
    def digitToBooleanValue(codigo):
        booleanValue = []
        for i in codigo:
            aux = False
            if i == 1:
                aux = True
            booleanValue.append(aux)
        return booleanValue
    
    def traducirCodigoEnElCircuito(booleanCode, sumandos):
        traductCodeEntrada = []
        for element in sumandos:
            j = 0
            auxForSumando = []
            for factor in element:
                if factor.isupper():
                    auxForSumando.append(not booleanCode[j])
                else:
                    auxForSumando.append(booleanCode[j])
                j += 1
            traductCodeEntrada.append(auxForSumando)
        return traductCodeEntrada
    
    def mostrarCodigoTraducido(e):
        formulaGeneralStr = formula(mat)
        PATRON = r"\w+"
        sumandos = re.findall(PATRON, formulaGeneralStr)
        codigo = agregarCodigo(e)
        booleanCode = digitToBooleanValue(codigo)
        codigoTraducido.value = traducirCodigoEnElCircuito(booleanCode, sumandos)
        page.update()

    def comprobarValorDelCircuito(traductCodeEntrada):
        productoLogico = []
        for element in traductCodeEntrada:
            productoLogico.append(element[0] and element[1] and element[2] and element[3])

        if True in productoLogico:
            return True
        else:
            return False
    
    def mostrarComprobar(e):
        formulaGeneralStr = formula(mat)
        PATRON = r"\w+"
        sumandos = re.findall(PATRON, formulaGeneralStr)
        codigo = agregarCodigo(e)
        booleanCode = digitToBooleanValue(codigo)
        comprobar = comprobarValorDelCircuito(traducirCodigoEnElCircuito(booleanCode, sumandos))
        animarFoco(comprobar)
        page.update()

    #Contenido de la pag
    formulaGeneralTxt = ft.Text()
    comprobarTxt = ft.Text()
    codigoTraducido = ft.Text()
    tb = ft.TextField(label="Salida")
    codigoTxt = ft.TextField(label="Codigo")

    boton = ft.ElevatedButton(text="Enviar", on_click=agregarSalida)
    boton2 = ft.ElevatedButton(text="Generar Salida", on_click=mostrarSalida)
    enviar2 = ft.ElevatedButton(text="Enviar", on_click=agregarCodigo)
    botonFormula = ft.ElevatedButton(text="Mostrar Fórmula", on_click=mostrarFormula)
    botonComprobar = ft.ElevatedButton(text="Comprobar", on_click=mostrarComprobar)
    botonMostrarCodigoTraducido = ft.ElevatedButton(text="Codigo Traducido", on_click=mostrarCodigoTraducido)
    lv = ft.ListView(expand=1, spacing=10, auto_scroll=True)

    foco = ft.Container(
        bgcolor="black",
        width=50,
        height = 50,
        border_radius=50,
        margin=ft.margin.all(0),
        animate=ft.animation.Animation(500, "bounceOut")
    )

    def animarFoco(valor):
        if valor:
            foco.bgcolor = "yellow"
        else:
            foco.bgcolor = "black"
        foco.update()

    page.add(
        ft.Row(
            [
                ft.Container(
                    ft.Column(
                        [ 
                            ft.Row(
                                [
                                    tb, boton
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_EVENLY
                            ),
                            ft.Container(
                                boton2,
                                margin=ft.margin.symmetric(vertical=20, horizontal=40),
                                alignment=ft.alignment.center
                            ),
                            ft.Container(
                                lv,
                                padding=ft.padding.symmetric(vertical=10, horizontal=140),
                                bgcolor=ft.colors.GREY_200,
                                border_radius=10,
                                margin=ft.margin.symmetric(vertical=20, horizontal=40),
                                alignment=ft.alignment.center
                            ),
                            ft.Container(
                                ft.Column(
                                    [
                                        botonFormula, formulaGeneralTxt
                                    ]
                                ),
                                margin=ft.margin.symmetric(vertical=20, horizontal=40),
                                alignment=ft.alignment.center_left
                            )
                        ]
                    ),
                    bgcolor=ft.colors.GREY,
                    border_radius=20,
                    width=500,
                    height=1000,
                    padding=ft.padding.symmetric(vertical=30),
                    alignment=ft.alignment.center
                ),
                ft.Container(
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    codigoTxt, enviar2 
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            ft.Container(
                                ft.Column(
                                    [
                                        botonMostrarCodigoTraducido, codigoTraducido
                                    ]
                                ),
                                margin=ft.margin.symmetric(vertical=30)
                            ),
                            ft.Container(
                                ft.Row(
                                    [
                                        botonComprobar, 
                                        ft.Column(
                                            [
                                                foco,
                                                ft.Container(
                                                    width=20,
                                                    height=30,
                                                    bgcolor=ft.colors.BLACK12,
                                                    alignment=ft.alignment.center,
                                                    margin=ft.margin.symmetric(horizontal=15)   
                                                )
                                            ],
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                        )
                                    ],
                                ),
                                margin=ft.margin.symmetric(vertical=30)    
                            ),
                                           
                        ]
                    ),
                    bgcolor=ft.colors.GREY,
                    border_radius=20,
                    width=500,
                    height=1000,
                    padding=ft.padding.symmetric(vertical=30, horizontal=30),
                    margin=ft.margin.symmetric(horizontal=20),
                    alignment=ft.alignment.center
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

ft.app(target=main)