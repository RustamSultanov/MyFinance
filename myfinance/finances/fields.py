from django.forms import DateField


class DateRangeField(DateField):
    def to_python(self, value):
        values = value.split(' - ')
        from_date = super(DateRangeField, self).to_python(values[0])
        to_date = super(DateRangeField, self).to_python(values[1])
        return from_date, to_date
