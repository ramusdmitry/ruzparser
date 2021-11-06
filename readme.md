#Structer of schedule:

## json_array:

Json response has 3 objects:
* Times
* Data
* Semestr

###Day
* **DayNumber** - *number of week (0 to 3)*
* **Time**
    * Time - *number of lessons (1 to 7)*
    * Code *???*
    * TimeFrom - *start of lesson*
    * TimeTo - *end of lesson*
    * **Class**
        * Code *???*
        * Name - *subject*
        * TeacherFull - *no comments*
        * Teacher - *no comments*
        * **Group**
            * Code *???*
            * Name - *name of group*
        * **Room**
            * Code *???*
            * Name - *number of room*
