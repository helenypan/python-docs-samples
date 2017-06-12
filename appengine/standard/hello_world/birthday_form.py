# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2

form = '''
<form method="POST">
    What is your birthday?
    <br>
    <label>
        Month
        <input type="text" name="month" value="%(month)s">
    </label>
    <label>
        Day
        <input type="text" name="day" value="%(day)s">
    </label>
    <label>
        Year
        <input type="text" name="year" value="%(year)s">
    </label>
    <div style="color:red">%(error)s</div>
    <input type="submit">
</form>
'''


def valid_year(year):
    if year and year.isdigit():
        if int(year) > 1900 and int(year)<2020:
            return year
    return None


def valid_day(day):
    if day and day.isdigit():
        day = int(day)
        if day >0 and day <= 31:
            return day

    return None


def valid_month(month):
    months = ['January',
              'February',
              'March',
              'April',
              'May',
              'June',
              'July',
              'August',
              'September',
              'October',
              'November',
              'December']

    month_abbvs = dict([(m[:3].lower(), m) for m in months])
    if month:
        short_m = month[:3].lower()
        return month_abbvs.get(short_m)
    return None


def escape(s, quote=None):
    '''Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true, the quotation mark character (")
is also translated.'''
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
    return s


class MainPage(webapp2.RequestHandler):
    def write_form(self, error="", month="", day="", year=""):
        self.response.out.write(form % {"error":error,
                                        "month":month,
                                        "day":day,
                                        "year":year})

    def get(self):
        # default content type is text/html
        # self.response.headers['Content-Type'] = 'text/html'
        self.write_form()

    def post(self):
        user_month = self.request.get("month")
        user_day = self.request.get('day')
        user_year = self.request.get("year")

        month = valid_month(user_month)
        day = valid_day(user_day)
        year = valid_year(user_year)

        if not (day and year and month):
            self.write_form("input not valid", escape(user_month), escape(user_day), escape(user_year))
        else:
            self.redirect("/thanks")


class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Thanks. That is a totally valid day!")

app = webapp2.WSGIApplication([
    ('/birthday', MainPage),
    ('/thanks', ThanksHandler)
], debug=True)
