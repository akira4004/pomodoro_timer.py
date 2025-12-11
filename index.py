import json
import random

# Импортируем твою логику из pomodoro_timer.py
workout_config = {
    "classic": {
        "name": "Классическая тренировка",
        "work_time": 20,
        "break_time": 5,
        "cycles": 4,
        "exercises": [
            {
                "name": "🔄 Разминка суставов",
                "description": "Вращения головой, плечами, локтями, кистями"
            },
            # ... добавь остальные упражнения из твоего кода
        ]
    }
}

def handler(event, context):
    """Обработчик для Яндекс Облака"""
    
    try:
        # Парсим запрос от Алисы
        request = event.get('request', {})
        session = event.get('session', {})
        state = session.get('state', {})
        
        # НОВЫЙ ПОЛЬЗОВАТЕЛЬ
        if request.get('command', '') == '':
            response_text = "🏃‍♂️ Добро пожаловать в утреннюю зарядку! Скажи 'меню'"
            
        elif 'меню' in request.get('command', '').lower():
            response_text = """🎯 Выберите тренировку:
            
1. Классическая (20/5)
2. Экспресс (10/2)
3. Для начинающих (5/5)"""
            
        elif 'классическая' in request.get('command', '').lower():
            workout = workout_config['classic']
            exercise = workout['exercises'][0]
            response_text = f"""🎯 Начинаем {workout['name']}!
            
Упражнение 1: {exercise['name']}
{exercise['description']}

⏰ Время: {workout['work_time']} мин
🔄 Циклов: {workout['cycles']}

Скажите "готово" когда выполните."""
            
        else:
            response_text = "Не поняла команду. Скажите 'меню'"
        
        # Формируем ответ для Алисы
        return {
            'version': '1.0',
            'session_state': state,
            'response': {
                'text': response_text,
                'end_session': False
            }
        }
        
    except Exception as e:
        return {
            'version': '1.0',
            'response': {
                'text': f'Ошибка: {str(e)}',
                'end_session': False
            }
        }
