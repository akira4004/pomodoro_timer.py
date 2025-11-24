import time
import json
import threading
import os
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
        self.current_cycle = 0
        self.current_mode = "work"
        self.remaining_time = 0
        self.thread = None
        self.current_exercise = None
        
    def _get_random_exercise(self):
        """Получить случайное упражнение из списка"""
        if self.exercises:
            return random.choice(self.exercises)
        return {"name": "💪 Упражнения", "description": "Выполняйте ваши обычные упражнения"}
        
    def start(self):
        if self.is_running:
            print("❌ Таймер уже запущен")
            return
        self.is_running = True
        self.thread = threading.Thread(target=self._run_timer)
        self.thread.daemon = True
        self.thread.start()
        
    def _run_timer(self):
        print(f"\n🎯 ЗАПУСК {self.name}")
        print(f"📊 Циклов: {self.cycles}")
        
        # Показываем все упражнения перед началом
        if self.exercises:
            print(f"\n📋 ПЛАН УПРАЖНЕНИЙ:")
            for i, exercise in enumerate(self.exercises, 1):
                print(f"   {i}. {exercise['name']}")
            print(f"\n💡 В каждом цикле будет выбрано случайное упражнение")
            input("\n↵ Нажмите Enter чтобы начать тренировку...")
        
        for cycle in range(1, self.cycles + 1):
            if not self.is_running: break
            self.current_cycle = cycle
            
            if self.is_running:
                self.current_mode = "work"
                self.current_exercise = self._get_random_exercise()
                success = self._run_phase("💪 УПРАЖНЕНИЯ", self.work_duration, cycle)
                if not success: break
            
            if self.is_running and cycle < self.cycles:
                self.current_mode = "break"
                success = self._run_phase("☕ ОТДЫХ", self.break_duration, cycle)
                if not success: break
        
        if self.is_running:
            print("\n🎉 ТРЕНИРОВКА ЗАВЕРШЕНА! Отличная работа! 🎉")
            self.is_running = False
    
    def _run_phase(self, phase_name, duration, cycle):
        self.remaining_time = duration
        start_time = time.time()
        
        print(f"\n⏰ {phase_name} - Цикл {cycle}/{self.cycles}")
        
        # Показываем упражнение в фазе работы
        if phase_name == "💪 УПРАЖНЕНИЯ" and self.current_exercise:
            print(f"🎯 {self.current_exercise['name']}")
            print(f"📝 {self.current_exercise['description']}")
        
        print(f"🕐 Длительность: {self._format_time(duration)}")
        
        try:
            while self.remaining_time > 0 and self.is_running:
                mins, secs = divmod(self.remaining_time, 60)
                time_display = f"{mins:02d}:{secs:02d}"
                progress = (duration - self.remaining_time) / duration
                bars = int(progress * 30)
                progress_bar = "[" + "█" * bars + "▒" * (30 - bars) + "]"
                print(f'\r{progress_bar} {time_display} осталось', end='', flush=True)
                time.sleep(1)
                elapsed = time.time() - start_time
                self.remaining_time = max(0, duration - int(elapsed))
                
            if self.is_running:
                print(f"\r✅ {phase_name} завершены!{' '*20}")
                print("\a", end='', flush=True)
                time.sleep(1)
                return True
            return False
        except KeyboardInterrupt:
            self.stop()
            return False
    
    def stop(self):
        if self.is_running:
            self.is_running = False
            print(f"\n\n⏹️ Таймер остановлен")
    
    def _format_time(self, seconds):
        if seconds < 60: return f"{seconds} сек"
        else: return f"{seconds // 60} мин"

class PomodoroManager:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.presets = self._load_config()
        self.current_timer = None
        
    def _load_config(self):
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            return config["pomodoroPresets"]
        except FileNotFoundError:
            print(f"❌ Файл {self.config_file} не найден")
            return []
    
    def list_presets(self):
        print("\n📋 ДОСТУПНЫЕ РЕЖИМЫ:")
        print("-" * 50)
        for i, preset in enumerate(self.presets, 1):
            work_min = preset['workDuration'] // 60
            break_min = preset['breakDuration'] // 60
            
            print(f"{i}. 🎯 {preset['name']}")
            print(f"   ⏱️  Упражнения: {work_min} мин | Отдых: {break_min} мин")
            print(f"   🔄 Циклов: {preset['cycles']}")
            print(f"   📝 {preset['description']}")
            
            # Показываем упражнения режима
            if 'exercises' in preset and preset['exercises']:
                print(f"   💪 Упражнения:")
                for exercise in preset['exercises']:
                    print(f"      • {exercise['name']}")
            
            print()
    
    def create_timer(self, preset_id):
        preset = next((p for p in self.presets if p['id'] == preset_id), None)
        if preset:
            exercises = preset.get('exercises', [])
            return PomodoroTimer(
                work_duration=preset['workDuration'],
                break_duration=preset['breakDuration'],
                cycles=preset['cycles'],
                name=preset['name'],
                exercises=exercises
            )
        return None
    
    def start_timer_by_id(self, preset_id):
        if self.current_timer and self.current_timer.is_running:
            print("❌ Уже запущен другой таймер")
            return False
        self.current_timer = self.create_timer(preset_id)
        if self.current_timer:
            self.current_timer.start()
            return True
        return False
    
    def stop_current_timer(self):
        if self.current_timer:
            self.current_timer.stop()
            self.current_timer = None
