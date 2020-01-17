#!/usr/bin/env python3
#
# A library that allows to create an inline calendar keyboard.
# grcanosa https://github.com/grcanosa
#
"""
Base methods for calendar keyboard creation and processing.
"""


from telegram import InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardRemove
import datetime
import calendar

def create_callback_data(action,year,month,day):
    """ Create the callback data associated to each button"""
    return ";".join([action,str(year),str(month),str(day)])

def separate_callback_data(data):
    """ Separate the callback data"""
    return data.split(";")

def create_callback_year(year=None,month=None):
    now = datetime.datetime.now()
    if year == None: year = now.year
    if month == None: month = now.month
    data_ignore = create_callback_data("IGNORE", year, month, 0)
    keyboard =[]
    # row = []
    # row.append(InlineKeyboardButton("<", callback_data=create_callback_data("PREV-YEAR", year, month, 1)))
    # row.append(InlineKeyboardButton("{}".format(year), callback_data=create_callback_data("SHOW-CALENDAR", year, month, 1)))#create_calendar(year, month)))
    # row.append(InlineKeyboardButton(">", callback_data=create_callback_data("NEXT-YEAR", year, month, 1)))
    # keyboard.append(row)

    curr_year=year
    for x in range(3):
        row = []
        for y in range(4):
            row.append(InlineKeyboardButton("{}".format(year), callback_data=create_callback_data("SHOW-CALENDAR", year, month, 1)))
            year+=1
        keyboard.append(row)

    year -= 1
    row = []
    row.append(InlineKeyboardButton("<", callback_data=create_callback_data("PREV-TWELVE", year, month, 1)))
    row.append(InlineKeyboardButton("{}".format(curr_year), callback_data=create_callback_data("SHOW-CALENDAR", curr_year, month, 1)))#create_calendar(year, month)))
    row.append(InlineKeyboardButton(">", callback_data=create_callback_data("NEXT-TWELVE", year, month, 1)))
    keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

def create_callback_month(year=None, month=None):
    now = datetime.datetime.now()
    if year == None: year = now.year
    if month == None: month = now.month
    data_ignore = create_callback_data("IGNORE", year, month, 0)
    keyboard = []
    count=0
    for x in range(3):
        row = []
        for y in range(4):
            count+=1
            row.append(InlineKeyboardButton(calendar.month_name[count], callback_data=create_callback_data("SHOW-CALENDAR", year, count, 1)))
        keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)

def create_calendar(year=None,month=None):
    """
    Create an inline keyboard with the provided year and month
    :param int year: Year to use in the calendar, if None the current year is used.
    :param int month: Month to use in the calendar, if None the current month is used.
    :return: Returns the InlineKeyboardMarkup object with the calendar.
    """
    now = datetime.datetime.now()
    if year == None: year = now.year
    if month == None: month = now.month
    data_ignore = create_callback_data("IGNORE", year, month, 0)
    keyboard = []
    #First row - Month and Year
    row=[]
    row.append(InlineKeyboardButton(calendar.month_name[month],callback_data=create_callback_data("SHOW-MONTH", year, month, 1)))#create_callback_year(year, month)))
    row.append(InlineKeyboardButton(str(year),callback_data=create_callback_data("SHOW-YEAR", year, month, 1)))
    keyboard.append(row)
    #Second row - Week Days
    row=[]
    for day in ["Mo","Tu","We","Th","Fr","Sa","Su"]:
        row.append(InlineKeyboardButton(day,callback_data=data_ignore))
    keyboard.append(row)

    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        row=[]
        for day in week:
            if(day==0):
                row.append(InlineKeyboardButton(" ",callback_data=data_ignore))
            else:
                row.append(InlineKeyboardButton(str(day),callback_data=create_callback_data("DAY",year,month,day)))
        keyboard.append(row)
    #Last row - Buttons
    row=[]
    row.append(InlineKeyboardButton("<",callback_data=create_callback_data("PREV-MONTH",year,month,day)))
    row.append(InlineKeyboardButton(" ",callback_data=data_ignore))
    row.append(InlineKeyboardButton(">",callback_data=create_callback_data("NEXT-MONTH",year,month,day)))
    keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)


def process_calendar_selection(bot,update):
    """
    Process the callback_query. This method generates a new calendar if forward or
    backward is pressed. This method should be called inside a CallbackQueryHandler.
    :param telegram.Bot bot: The bot, as provided by the CallbackQueryHandler
    :param telegram.Update update: The update, as provided by the CallbackQueryHandler
    :return: Returns a tuple (Boolean,datetime.datetime), indicating if a date is selected
                and returning the date if so.
    """
    ret_data = (False,None)
    query = update.callback_query
    (action,year,month,day) = separate_callback_data(query.data)
    curr = datetime.datetime(int(year), int(month), 1)
    curr_year = datetime.datetime(int(year), int(month), 1).year
    curr_month = datetime.datetime(int(year), int(month), 1).month
    if action == "IGNORE":
        bot.answer_callback_query(callback_query_id= query.id)
    elif action == "DAY":
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id
            )
        ret_data = True,datetime.datetime(int(year),int(month),int(day))
    elif action == "PREV-MONTH":
        pre = curr - datetime.timedelta(days=1)
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=create_calendar(int(pre.year),int(pre.month)))
    elif action == "NEXT-MONTH":
        ne = curr + datetime.timedelta(days=31)
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=create_calendar(int(ne.year), int(ne.month)))
    elif action == "PREV-YEAR":
        pre = curr_year - 1  #datetime.timedelta(days=1)
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=create_callback_year(int(pre), int(curr_month)))
    elif action == "NEXT-YEAR":
        ne = curr_year + 1  #datetime.timedelta(days=31)
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=create_callback_year(int(ne), int(curr_month)))
    elif action == "PREV-TWELVE":
        pre = curr_year - 23  #datetime.timedelta(days=1)
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=create_callback_year(int(pre), int(curr_month)))
    elif action == "NEXT-TWELVE":
        ne = curr_year + 1   #datetime.timedelta(days=31)
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=create_callback_year(int(ne), int(curr_month)))
    elif action == "SHOW-YEAR":
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=create_callback_year(int(curr_year), int(curr_month)))
    elif action == "SHOW-MONTH":
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=create_callback_month(int(curr_year), int(curr_month)))
    elif action == "SHOW-CALENDAR":
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=create_calendar(int(curr_year), int(curr_month)))
    else:
        bot.answer_callback_query(callback_query_id= query.id,text="Something went wrong!")
        # UNKNOWN
    return ret_data
