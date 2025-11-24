import time
import json
import random
from datetime import datetime

class PomodoroTimer:
    def __init__(self, work_duration, break_duration, cycles=4, name="Pomodoro", exercises=None):
        self.work_duration = work_duration
        self.break_duration = break_duration
        self.cycles = cycles
        self.name = name
        self.exercises = exercises or []
        self.is_running = False
        
    def _get_random_exercise(self):
        """Выбирает случайное упражнение из списка"""
        if self.exercises:
            return random.choice(self.exercises)
        return {"name": "💪 Упражнения", "description": "Выполняйте ваши обычные упражнения"}
        
    def start(self):
        """Запуск таймера"""
        if self.is_running:
            print("❌ Таймер уже запущен")
            return False
            
        self.is_running = True
        print(f"\n🎯 ЗАПУСК {self.name}")
        if self.exercises:
            print(f"📋 В программе: {len(self.exercises)} упражнений")
        print(f"📊 Всего циклов: {self.cycles}")
        
        # Показываем все упражнения перед началом
        if self.exercises:
            print(f"\n📖 ПРОГРАММА ТРЕНИРОВКИ:")
            for i, exercise in enumerate(self.exercises, 1):
                print(f"   {i}. {exercise['name']}")
        
        input("\n↵ Нажмите Enter чтобы начать тренировку...")
        
        # ОСНОВНОЙ ЦИКЛ ТАЙМЕРА
        for cycle in range(1, self.cycles + 1):
            if not self.is_running: 
                break
                
            print(f"\n{'='*60}")
            print(f"🔄 ЦИКЛ {cycle}/{self.cycles}")
            print(f"{'='*60}")
            
            # Выбираем случайное упражнение
            exercise = self._get_random_exercise()
            
            # ФАЗА РАБОТЫ
            if self.is_running:
                print(f"\n💪 УПРАЖНЕНИЕ: {exercise['name']}")
                print(f"📝 {exercise['description']}")
                print(f"⏰ Время: {self._format_time(self.work_duration)}")
                
                if not self._countdown("РАБОТА", self.work_duration):
                    break
            
            # ФАЗА ОТДЫХА (кроме последнего цикла)
            if self.is_running and cycle < self.cycles:
                print(f"\n☕ ПЕРЕРЫВ")
                print(f"⏰ Время: {self._format_time(self.break_duration)}")
                
                if not self._countdown("ОТДЫХ", self.break_duration):
                    break
        
        if self.is_running:
            print(f"\n{'='*60}")
            print("🎉 ТРЕНИРОВКА ЗАВЕРШЕНА! Отличная работа! 🎉")
            print(f"{'='*60}")
            self.is_running = False
            return True
        return False
    
    def _countdown(self, phase_name, duration):
        """Отсчет времени с прогресс-баром"""
        start_time = time.time()
        remaining = duration
        
        try:
            while remaining > 0 and self.is_running:
                elapsed = time.time() - start_time
                remaining = max(0, duration - int(elapsed))
                
                mins, secs = divmod(remaining, 60)
                time_display = f"{mins:02d}:{secs:02d}"
                
                # Прогресс-бар
                progress = (duration - remaining) / duration
                bars = int(progress * 30)
                progress_bar = "[" + "█" * bars + "▒" * (30 - bars) + "]"
                
                print(f'\r{progress_bar} {time_display} осталось', end='', flush=True)
                time.sleep(0.1)  # Частое обновление
                
            if self.is_running:
                print(f"\r✅ {phase_name} завершена!{' '*30}")
                print("\a")  # Звуковой сигнал
                time.sleep(1)
                return True
            return False
            
        except KeyboardInterrupt:
            self.stop()
            return False
    
    def stop(self):
        """Остановка таймера"""
        if self.is_running:
            self.is_running = False
            print(f"\n\n⏹️ Таймер остановлен")
    
    def _format_time(self, seconds):
        """Форматирование времени"""
        if seconds < 60: 
            return f"{seconds} сек"
        else: 
            minutes = seconds // 60
            return f"{minutes} мин"

class PomodoroManager:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.presets = self._load_config()
        self.current_timer = None
        
    def _load_config(self):
        """Загрузка конфигурации"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"✅ Загружено {len(config['pomodoroPresets'])} режимов тренировки")
            return config["pomodoroPresets"]
        except FileNotFoundError:
            print(f"❌ Файл {self.config_file} не найден")
            return []
        except json.JSONDecodeError:
            print(f"❌ Ошибка в файле конфигурации")
            return []
    
    def list_presets(self):
        """Список всех режимов"""
        print("\n📋 ДОСТУПНЫЕ РЕЖИМЫ ТРЕНИРОВКИ:")
        print("=" * 60)
        for i, preset in enumerate(self.presets, 1):
            work_min = preset['workDuration'] // 60
            break_min = preset['breakDuration'] // 60
            
            print(f"\n{i}. 🎯 {preset['name']}")
            print(f"   ⏱️  Упражнения: {work_min} мин | Отдых: {break_min} мин")
            print(f"   🔄 Циклов: {preset['cycles']}")
            print(f"   📝 {preset['description']}")
            
            if 'exercises' in preset and preset['exercises']:
                print(f"   💪 Упражнения: {len(preset['exercises'])} видов")
                for j, exercise in enumerate(preset['exercises'][:3], 1):  # Показываем первые 3
                    print(f"      {j}. {exercise['name']}")
                if len(preset['exercises']) > 3:
                    print(f"      ... и еще {len(preset['exercises']) - 3}")
            
            if preset['id'] == 'quick_test':
                print(f"   🧪 [ТЕСТОВЫЙ РЕЖИМ - для проверки]")
        
        print("\n" + "=" * 60)
    
    def show_exercise_details(self, preset_id):
        """Детали упражнений для выбранного режима"""
        preset = next((p for p in self.presets if p['id'] == preset_id), None)
        if preset and 'exercises' in preset:
            print(f"\n📖 ПОДРОБНАЯ ПРОГРАММА: {preset['name']}")
            print("=" * 60)
            for i, exercise in enumerate(preset['exercises'], 1):
                print(f"\n{i}. {exercise['name']}")
                print(f"   📝 {exercise['description']}")
            print("\n" + "=" * 60)
            return True
        else:
            print("❌ Для этого режима нет описаний упражнений")
            return False
    
    def create_timer(self, preset_id):
        """Создание таймера"""
        preset = next((p for p in self.presets if p['id'] == preset_id), None)
        if preset:
            exercises = preset.get('exercises', [])
            timer = PomodoroTimer(
                work_duration=preset['workDuration'],
                break_duration=preset['breakDuration'],
                cycles=preset['cycles'],
                name=preset['name'],
                exercises=exercises
            )
            return timer
        return None
    
    def start_timer_by_id(self, preset_id):
        """Запуск таймера"""
        if self.current_timer and self.current_timer.is_running:
            print("❌ Уже запущен другой таймер")
            return False
        
        self.current_timer = self.create_timer(preset_id)
        if self.current_timer:
            # Показываем упражнения перед запуском
            self.show_exercise_details(preset_id)
            input("\n↵ Нажмите Enter чтобы начать...")
            return self.current_timer.start()
        return False
    
    def stop_current_timer(self):
        """Остановка таймера"""
        if self.current_timer:
            self.current_timer.stop()
            self.current_timer = None
        else:
            print("❌ Нет активного таймера")
