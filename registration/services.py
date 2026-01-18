from datetime import datetime, timedelta
from organisation.models import Record
from registration.models import Registration

def get_free_records(
    date_registration, time_registration, min_capacity=1
):
    """Возвращает свободные записи, учитывая фиксированную длительность 30 минут"""
    requested_start = datetime.combine(date_registration, time_registration)
    requested_end = requested_start + timedelta(minutes=30)  # длительность услуги - 30 минут

    now = datetime.now()

    # Проверка, что выбранное время не в прошлом
    if requested_start < now:
        return Record.objects.none()

    # Получаем все регистрации на выбранную дату
    registrations = Registration.objects.filter(date_registration=date_registration)

    occupied_record_ids = set()

    for registration in registrations:
        # Проверка существования связанного Record
        if not hasattr(registration, 'registration') or registration.registration is None:
            continue

        res_start = datetime.combine(
            registration.date_registration, registration.time_registration
        )
        res_end = res_start + timedelta(minutes=30)  # всегда 30 минут

        # Проверка пересечения интервалов
        if (requested_start < res_end) and (res_start < requested_end):
            occupied_record_ids.add(registration.registration.id)

    # Возвращает свободные услуги, учитывая вместимость
    available_records = Record.objects.exclude(id__in=occupied_record_ids).filter(
        record_capacity__gte=min_capacity
    )
    return available_records
