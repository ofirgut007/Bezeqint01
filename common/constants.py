SORT_DIR_VALUES = ('asc', 'desc')

DAYS = (
    'SUN','MON','TUE','WED','THU','FRI','SAT'
)
ALERT_TEMPLATE = (
    'id', 'status', 'day', 'time',
    )

ALERT_SINGLE = (
    'alert_template_id',
    'created_at', 'updated_at',
)

NOTIFICATION = (
    'id','status', 'day', 'time', 
)

NOTIFICATION_ALERT = (
    'alert_single_id',
    'notification_id',
    'status',
)