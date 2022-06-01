import datetime
import requests
import os
import argparse
import re
import json
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd, FR
from holidays. constants import JAN, MAY, AUG, OCT, NOV, DEC
from holidays.holiday_base import HolidayBase


class FiestaEcuador(HolidayBase):
    """
    La clase principal es (FiestaEcuador) ya que seda el feriado en Ecuador 
    Su objetivo es determinar la fecha específica y conocer la vacaciones 
    de una forma más rápido y flexible posible.
    https://www.turismo.gob.ec/wp-content/uploads/2020/03/CALENDARIO-DE-FERIADOS.pdf
    ...
    Atributos (Hereda la clase HolidayBase)
    ----------
    prov: str
        código de provincia según ISO3166-2
    Metodo
    -------
    __init__(self, plate, fecha, tiempo, online=False):
        Construye todos los atributos necesarios para el objeto FiestaEcuador.
    _poblar(uno mismo, año):
        Devoluciones si una fecha es feriado o no
    """     
    # Códigos ISO 3166-2 para las principales subdivisiones,
    # provincias llamadas
    # https://es.wikipedia.org/wiki/ISO_3166-2:EC
    Provincia = ["EC-P"]  # TODO podra añadir mas provincias que tiene en el ecuador 
    def __init__(self, **kwargs):     
        self.country = "ECU"
        self.prov = kwargs.pop("provincia", "ON")
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, anos):
        # Día de Año Nuevo
        self[datetime.fecha(anos, JAN, 1)] = "Año Nuevo [Día de Año Nuevo]" 
        #Navidad
        self[datetime.fecha(anos, DEC, 25)] = "Navidad [Navidad]"  
        # semana Santa
        self[easter(anos) + rd(weekday=FR(-1))] = "Semana Santa (Viernes Santo) [Buen viernes)]  "
        self[easter(anos)] = "Día de Pascuas [Día de Pascua]" 
        # Carnaval
        total_prestado_dias = 46
        self[easter(anos) - datetime.timedelta(dias=total_prestado_dias+2)],="Lunes de carnaval [Carnaval del lunes)]"
        self[easter(anos) - datetime.timedelta(dias=total_prestado_dias+1)] = "Martes de carnaval [Martes de Carnaval)]"
        #Dia laboral
        nombre = "Día Nacional del Trabajo [Día del Trabajo]"
       # (Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016 /R.O # 906)) Si el feriado cae en sábado o martes
        # el descanso obligatorio irá al viernes o lunes inmediato anterior
        # respectivamente
        if anos > 2015 and datetime.fecha(anos, MAY, 1).weekday() in (5,1):
            self[datetime.fecha(anos, MAY, 1) - datetime.timedelta(dias=1)] = nombre 
        # (Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016/R.O # 906)) si el feriado cae en domingo
        # el descanso obligatorio sera para el lunes siguiente
        elif anos > 2015 and datetime.fecha(anos, MAY, 1).weekday() == 6:
            self[datetime.fecha(anos, MAY, 1) + datetime.timedelta(dias=1)] = nombre 
        # (Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016 /R.O # 906)) Feriados que sean en miércoles o jueves
        # se moverá al viernes de esa semana
        elif anos > 2015 and  datetime.fecha(anos, MAY, 1).weekday() in (2,3):
            self[datetime.fecha(anos, MAY, 1) + rd(weekday=FR)] = nombre 
        else:
            self[datetime.fecha(anos, MAY, 1)] = nombre 
        
        # Pichincha battle, the rules are the same as the labor day
        nombre  = "Batalla del Pichincha [Pichincha Battle]"
        if anos > 2015 and datetime.fecha(anos, MAY, 24).weekday() in (5,1):
            self[datetime.fecha(anos, MAY, 24).weekday() - datetime.timedelta(dias=1)] = nombre 
        elif anos > 2015 and datetime.fecha(anos, MAY, 24).weekday() == 6:
            self[datetime.fecha(anos, MAY, 24) + datetime.timedelta(dias=1)] = nombre 
        elif anos > 2015 and  datetime.fecha(anos, MAY, 24).weekday() in (2,3):
            self[datetime.fecha(anos, MAY, 24) + rd(weekday=FR)] = nombre 
        else:
            self[datetime.fecha(anos, MAY, 24)] = nombre 
        
        # First Cry of Independence, the rules are the same as the labor day
        nombre  = "Primer Grito de la Independencia [First Cry of Independence]"
        if anos > 2015 and datetime.fecha(anos, AUG, 10).weekday() in (5,1):
            self[datetime.fecha(anos, AUG, 10)- datetime.timedelta(dias=1)] = nombre 
        elif anos > 2015 and datetime.fecha(anos, AUG, 10).weekday() == 6:
            self[datetime.fecha(anos, AUG, 10) + datetime.timedelta(dias=1)] = nombre 
        elif anos > 2015 and  datetime.fecha(anos, AUG, 10).weekday() in (2,3):
            self[datetime.fecha(anos, AUG, 10) + rd(weekday=FR)] = nombre 
        else:
            self[datetime.fecha(anos, AUG, 10)] = nombre    
        
        # Independencia de Guayaquil, las reglas son las mismas que el día del trabajo
        nombre = "Independencia de Guayaquil [Independencia de Guayaquil]"
        if anos > 2015 and datetime.fecha(anos, OCT, 9).weekday() in (5,1):
            self[datetime.fecha(anos, OCT, 9) - datetime.timedelta(dias=1)] = nombre 
        elif anos > 2015 and datetime.fecha(anos, OCT, 9).weekday() == 6:
            self[datetime.fecha(anos, OCT, 9) + datetime.timedelta(dias=1)] = nombre 
        elif anos > 2015 and  datetime.fecha(anos, MAY, 1).weekday() in (2,3):
            self[datetime.fecha(anos, OCT, 9) + rd(weekday=FR)] = nombre 
        else:
            self[datetime.fecha(anos, OCT, 9)] = nombre         
        
        # Day of the Dead and
        nombredd = "Día de los difuntos [Dia de los Muertos]"
        # Independence of Cuenca
        nombreic = "Independencia de Cuenca [Independence of Cuenca]"
        #(Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016/R.O # 906))
        #Para festivos nacionales y/o locales que coincidan en días corridos,
        #se aplicarán las siguientes reglas:
        if (datetime.fecha(anos, NOV, 2).weekday() == 5 and  datetime.fecha(anos, NOV, 3).weekday() == 6):
            self[datetime.fecha(anos, NOV, 2) - datetime.timedelta(dias=1)] = nombredd
            self[datetime.fecha(anos, NOV, 3) + datetime.timedelta(dias=1)] = nombreic     
        elif (datetime.fecha(anos, NOV, 3).weekday() == 2):
            self[datetime.fecha(anos, NOV, 2)] = nombredd
            self[datetime.fecha(anos, NOV, 3) - datetime.timedelta(dias=2)] = nombreic
        elif (datetime.fecha(anos, NOV, 3).weekday() == 3):
            self[datetime.fecha(anos, NOV, 3)] = nombreic
            self[datetime.fecha(anos, NOV, 2) + datetime.timedelta(dias=2)] = nombredd
        elif (datetime.fecha(anos, NOV, 3).weekday() == 5):
            self[datetime.fecha(anos, NOV, 2)] =  nombredd
            self[datetime.fecha(anos, NOV, 3) - datetime.timedelta(dias=2)] = nombreic
        elif (datetime.fecha(anos, NOV, 3).weekday() == 0):
            self[datetime.fecha(anos, NOV, 3)] = nombreic
            self[datetime.fecha(anos, NOV, 2) + datetime.timedelta(dias=2)] = nombredd
        else:
            self[datetime.fecha(anos, NOV, 2)] = nombredd
            self[datetime.fecha(anos, NOV, 3)] = nombreic  
            
        # Fundación de Quito, aplica solo para la provincia de Pichincha,
        # las reglas son las mismas que el día del trabajo
        nombre  = "Fundación de Quito [Fundación de Quito]"       
        if self.prov in ("EC-P"):
            if anos > 2015 and datetime.fecha(anos, DEC, 6).weekday() in (5,1):
                self[datetime.fecha(anos, DEC, 6) - datetime.timedelta(dias=1)] = nombre 
            elif anos > 2015 and datetime.fecha(anos, DEC, 6).weekday() == 6:
                self[(datetime.fecha(anos, DEC, 6).weekday()) + datetime.timedelta(dias=1)] =nombre 
            elif anos > 2015 and  datetime.fecha(anos, DEC, 6).weekday() in (2,3):
                self[datetime.fecha(anos, DEC, 6) + rd(weekday=FR)] = nombre 
            else:
                self[datetime.fecha(anos, DEC, 6)] = nombre 

class PicoPlaca:
    """
    Una clase para representar un vehículo.
    medida de restricción (Pico y Placa)
    - ORDENANZA METROPOLITANA N° 0305
    http://www7.quito.gob.ec/mdmq_ordenanzas/Ordenanzas/ORDENANZAS%20A%C3%91OS%20ANTERIORES/ORDM-305-%20%20CIRCULACION%20VEHICULAR%20PICO%20Y%20PLACA.pdf
    ...
    Atributo
    ----------
    plate : str 
        El registro o patente de un vehículo es una combinación de caracteres alfabéticos o numéricos
        caracteres que identifican e individualizan el vehículo respecto de los demás;
        
        El formato utilizado es
        XX-YYYY o XXX-YYYY,
        donde X es una letra mayúscula e Y es un dígito.
    fecha : str
        Fecha en la que el vehículo pretende transitar
        esta siguiendo el
        Formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22
    tiempo : str
        tiempo en que el vehículo pretende transitar
        esta siguiendo el formato
        HH:MM: por ejemplo, 08:35, 19:30
    online: boolean, optional
        if online == Cierto, se utilizará la API abstracta de días festivos
    Methods
    -------
    __init__(self, plate, fecha, tiempo, online=False):
        Construye todos los atributos necesarios.
        para el objeto PicoPlaca.
    plate(self):
        Obtiene el valor del atributo de placa
    plate(self, value):
        Establece el valor del atributo de la placa
    fecha(self):
        Obtiene el valor del atributo de fecha
    fecha(self, value):
        Establece el valor del atributo de fecha
    tiempo(self):
        Obtiene el valor del atributo de tiempo
    tiempo(self, value):
       Establece el valor del atributo de tiempo
    __find_day(self, date):
        Returns el día a partir de la fecha: por ejemplo, miércoles
    __is_forbidden_time(self, check_time):
        Returns True if provided time is inside the forbidden peak hours, otherwise False
    __is_holiday:
        Returns True if la fecha marcada (en formato ISO 8601 AAAA-MM-DD) es un día festivo en Ecuador, de lo contrario Falso
    predict(self):
        Returns True si el vehículo con la placa especificada puede estar en la carretera en la fecha y hora especificada, de lo contrario Falso
    """ 
    #Dias de la semana
    __dias = [
            "Lunes",
            "Martes",
            "Miércoles",
            "Jueves",
            "Viernes",
            "Sábado",
            "Domingo"]

   #Diccionario que contiene las restricciones de la forma {día: último dígito prohibido}
    __restrictions = {
            "Lunes": [1, 2],
            "martes": [3, 4],
            "Miércoles": [5, 6],
            "Jueves": [7, 8],
            "Viernes": [9, 0],
            "Sábado": [],
            "Domingo": []}

    def __init__(self, plate, fecha, tiempo, online=False):
        """
        Construye todos los atributos necesarios para el objeto PicoPlaca.
        Parameters
        ----------
            plate : str 
               El registro o patente de un vehículo es una combinación de caracteres alfabéticos o numéricos
                caracteres que identifican e individualizan el vehículo respecto de los demás;
                El formato utilizado es AA-YYYY o XXX-YYYY, donde X es una letra mayúscula e Y es un dígito.
            fecha : str
                Fecha en la que el vehículo pretende transitar
                Sigue el formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22.   
            tiempo : str
                tiempo en que el vehículo pretende transitar
                Sigue el formato HH:MM: por ejemplo, 08:35, 19:30    
            online: boolean, optional
                si en línea == Verdadero, se usará la API de días festivos abstractos (el valor predeterminado es Falso)   
             """                
        self.plate = plate
        self.fecha = fecha
        self.tiempo = tiempo
        self.online = online


    @property
    def plate(self):
        """Obtiene el valor del atributo de placa"""
        return self._plate


    @plate.setter
    def plate(self, value):
        """
        Establece el valor del atributo de la placa
        Parámetros
        ----------
        value : str
        
        Raises
        ------
        ValueError
            If value string is not formated as 
            XX-YYYY or XXX-YYYY, 
            where X is a capital letter and Y is a digit
        """
        if not re.match('^[A-Z]{2,3}-[0-9]{4}$', value):
            raise ValueError(
                'La placa debe tener el siguiente formato: XX-YYYY o XXX-YYYY, donde X es una letra mayúscula e Y es un dígito')
        self._plate = value


    @property
    def fecha(self):
        """Obtiene el valor del atributo de fecha"""
        return self._fecha


    @fecha.setter
    def fecha(self, value):
        """
        Establece el valor del atributo de fecha
        Parámetros
        ----------
        valor: cadena
        
        aumenta
        ------
        ValorError
            Si la cadena de valor no tiene el formato AAAA-MM-DD (por ejemplo, 2021-04-02)
        """
        try:
            if len(value) != 10:
                raise ValueError
            datetime.datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                'La fecha debe tener el siguiente formato: AAAA-MM-DD (por ejemplo: 2021-04-02)') from None
        self._fecha = value
        

    @property
    def tiempo(self):
        """Obtiene el valor del atributo de tiempo"""
        return self._tiempo


    @tiempo.setter
    def tiempo(self, value):
        """
        Sets the time attribute value
        Parameters
        ----------
        value : str
        
        Raises
        ------
        ValueError
            If value string is not formated as HH:MM (e.g., 08:31, 14:22, 00:01)
        """
        if not re.match('^([01][0-9]|2[0-3]):([0-5][0-9]|)$', value):
            raise ValueError(
                'The time must be in the following format: HH:MM (e.g., 08:31, 14:22, 00:01)')
        self._tiempo = value


    def __find_day(self, fecha):
        """
        Finds the day from the date: e.g., Wednesday
        Parameters
        ----------
        date : str
            It is following the ISO 8601 format YYYY-MM-DD: e.g., 2020-04-22
        Returns
        -------
        Returns the day from the date as a string
        """        
        d = datetime.datetime.strptime(fecha, '%Y-%m-%d').weekday()
        return self.__dias[d]


    def __is_forbidden_time(self, check_tiempo):
        """
        Checks if the time provided is within the prohibited peak hours,
        where the peak hours are: 07:00 - 09:30 and 16:00 - 19:30
        Parameters
        ----------
        check_time : str
            Time that will be checked. It is in format HH:MM: e.g., 08:35, 19:15
        Returns
        -------
        Returns True if provided time is inside the forbidden peak hours, otherwise False
        """           
        t = datetime.datetime.strptime(check_tiempo, '%H:%M').time()
        return ((t >= datetime.time(7, 0) and t <= datetime.time(9, 30)) or
                (t >= datetime.time(16, 0) and t <= datetime.time(19, 30)))


    def __is_holiday(self, fecha, online):
        """
        Checks if date (in ISO 8601 format YYYY-MM-DD) is a public holiday in Ecuador
        if online == True it will use a REST API, otherwise it will generate the holidays of the examined year
        
        Parameters
        ----------
        date : str
            It is following the ISO 8601 format YYYY-MM-DD: e.g., 2020-04-22
        online: boolean, optional
            if online == True the abstract public holidays API will be used        
        Returns
        -------
        Returns True if the checked date (in ISO 8601 format YYYY-MM-DD) is a public holiday in Ecuador, otherwise False
        """            
        y, m, d = fecha.split('-')

        if online:
            # abstractapi Holidays API, free version: 1000 requests per month
            # 1 request per second
            # retrieve API key from enviroment variable
            key = os.environ.get('HOLIDAYS_API_KEY')
            response = requests.get(
                "https://holidays.abstractapi.com/v1/?api_key={}&country=EC&year={}&month={}&day={}".format(key, y, m, d))
            if (response.status_code == 401):
                # This means there is a missing API key
                raise requests.HTTPError(
                    'Missing API key. Store your key in the enviroment variable HOLIDAYS_API_KEY')
            if response.content == b'[]':  # if there is no holiday we get an empty array
                return False
            # Fix Maundy Thursday incorrectly denoted as holiday
            if json.loads(response.text[1:-1])['nombre '] == 'Maundy Thursday':
                return False
            return True
        else:
            ecu_holidays = FiestaEcuador(prov='EC-P')
            return fecha in ecu_holidays


    def predict(self):
        """
        Checks if vehicle with the specified plate can be on the road on the provided date and time based on the Pico y Placa rules:
        http://www7.quito.gob.ec/mdmq_ordenanzas/Ordenanzas/ORDENANZAS%20A%C3%91OS%20ANTERIORES/ORDM-305-%20%20CIRCULACION%20VEHICULAR%20PICO%20Y%20PLACA.pdf    
        Returns
        -------
        Returns 
        True if the vehicle with 
        the specified plate can be on the road 
        at the specified date and time, otherwise False
        """
        # Check if date is a holiday
        if self.__is_holiday(self.fecha, self.online):
            return True

        # Check for restriction-excluded vehicles according to the second letter of the plate or if using only two letters
        # https://es.wikipedia.org/wiki/Matr%C3%ADculas_automovil%C3%ADsticas_de_Ecuador
        if self.plate[1] in 'AUZEXM' or len(self.plate.split('-')[0]) == 2:
            return True

        # Check if provided time is not in the forbidden peak hours
        if not self.__is_forbidden_time(self.tiempo):
            return True

        day = self.__find_day(self.fecha)  # Find day of the week from date
        # Check if last digit of the plate is not restricted in this particular day
        if int(self.plate[-1]) not in self.__restrictions[day]:
            return True

        return False


if __name__ == '__main__':

    online=False
    plate=input("Ingrese la placa Vehuculo XXX-YYYY :  ")
    fecha=input("Ingrese la fecha YYYY-MM-DD: ")
    tiempo=input("Ingrese la hora y el minuto HH:MM: ")
    pyp = PicoPlaca(plate,fecha, tiempo,online)


    if pyp.predict():
        print(
            'The vehicle with plate {} CAN be on the road on {} at {}.'.format(
                plate,
                fecha,
                tiempo))
    else:
        print(
            'The vehicle with plate {} CANNOT be on the road on {} at {}.'.format(
                plate,
                fecha,
                tiempo))