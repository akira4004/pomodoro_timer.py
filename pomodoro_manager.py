import time
import json
import threading
import os
from datetime import datetime
import sys

class PomodoroTimer:
    def __init__(self, work_duration, break_duration, cycles=4, name="Pomodoro"):
        self.work_duration = work_duration
        self.break_duration = break_duration
        self.cycles = cycles
        self.name = name
        self.is_running = False
        self.current_cycle = 0
        self.current_mode = "work"
        self.remaining_time = 0
        self.thread = None
        
    def _clear_line(self):
        """Очистка текущей строки в консоли"""
        print('\r' + ' ' * 80, end='\r', flush=True)
        
    def _print_header(self, text):
        """Красивый заголовок"""
        print(f"\n{'='*60}")
        print(f"🎯 {text}")
        print(f"{'='*60}")
        
    def start(self):
        """Запуск таймера в отдельном потоке"""
        if self.is_running:
            print("❌ Таймер уже запущен")
            return
            
        self.is_running = True
        self.thread = threading.Thread(target=self._run_timer)
        self.thread.daemon = True
        self.thread.start()
        
    def _run_timer(self):
        """Основная логика таймера"""
        self._print_header(f"ЗАПУСК {self.name}")
        print(f"📊 Всего циклов: {self.cycles}")
        
        for cycle in range(1, self.cycles + 1):
            if not self.is_running:
                break
                
            self.current_cycle = cycle
            
            # Фаза работы
            if self.is_running:
                self.current_mode = "work"
                success = self._run_phase("💪 УПРАЖНЕНИЯ", self.work_duration, cycle)
                if not success:
                    break
            
            # Фаза отдыха (кроме последнего цикла)
            if self.is_running and cycle < self.cycles:
                self.current_mode = "break"
                success = self._run_phase("☕ ОТДЫХ", self.break_duration, cycle)
                if not success:
                    break
        
        if self.is_running:
            self._print_header("ТРЕНИРОВКА ЗАВЕРШЕНА!")
            print("🎉 Отличная работа! Вы молодец! 🎉")
            print("💪 Продолжайте в том же духе!")
            self.is_running = False
    
    def _run_phase(self, phase_name, duration, cycle):
        """Запуск фазы (работа или отдых)"""
        self.remaining_time = duration
        start_time = time.time()
        
        print(f"\n⏰ {phase_name} - Цикл {cycle}/{self.cycles}")
        print(f"🕐 Длительность: {self._format_time(duration)}")
        print(f"🚀 Начало: {datetime.now().strftime('%H:%M:%S')}")
        print()
        
        try:
            while self.remaining_time > 0 and self.is_running:
                mins, secs = divmod(self.remaining_time, 60)
                time_display = f"{mins:02d}:{secs:02d}"
                
                # Прогресс-бар
                progress = (duration - self.remaining_time) / duration
                bars = int(progress * 30)
                progress_bar = "[" + "█" * bars + "▒" * (30 - bars) + "]"
                
                print(f'\r{progress_bar} {time_display} осталось', end='', flush=True)
                
                time.sleep(1)
                elapsed = time.time() - start_time
                self.remaining_time = max(0, duration - int(elapsed))
                
            if self.is_running:
                self._clear_line()
                print(f"✅ {phase_name} завершены!")
                self._play_sound_alert()
                time.sleep(1)  # Пауза между фазами
                return True
            else:
                return False
                
        except KeyboardInterrupt:
            self.stop()
            return False
    
    def _play_sound_alert(self):
        """Воспроизведение звукового сигнала"""
        try:
            # Системный beep
            print("\a", end='', flush=True)
        except:
            pass  # Игнорируем ошибки со звуком
    
    def stop(self):
        """Остановка таймера"""
        if self.is_running:
            self.is_running = False
            print(f"\n\n⏹️ Таймер '{self.name}' остановлен")
            if self.thread:
                self.thread.join(timeout=1)
    
    def pause(self):
        """Пауза таймера"""
        if self.is_running:
            self.is_running = False
            print(f"\n⏸️ Таймер на паузе")
    
    def resume(self):
        """Продолжение таймера"""
        if not self.is_running and self.remaining_time > 0:
            self.is_running = True
            print(f"\n▶️ Продолжение таймера")
            self.start()
    
    def get_status(self):
        """Получение текущего статуса"""
        status = {
            "name": self.name,
            "is_running": self.is_running,
            "current_cycle": self.current_cycle,
            "total_cycles": self.cycles,
            "current_mode": self.current_mode,
            "remaining_time": self.remaining_time,
            "progress": f"{self.current_cycle}/{self.cycles}"
        }
        return status
    
    def _format_time(self, seconds):
        """Форматирование времени в читаемый вид"""
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
        """Загрузка конфигураций из JSON файла"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"✅ Загружено {len(config['pomodoroPresets'])} конфигураций таймеров")
            return config["pomodoroPresets"]
        except FileNotFoundError:
            print(f"❌ Файл конфигурации {self.config_file} не найден")
            return []
        except json.JSONDecodeError:
            print(f"❌ Ошибка чтения JSON файла {self.config_file}")
            return []
    
    def list_presets(self):
        """Вывод списка доступных пресетов"""
        print("\n📋 ДОСТУПНЫЕ РЕЖИМЫ ТРЕНИРОВКИ:")
        print("-" * 60)
        
        for i, preset in enumerate(self.presets, 1):
            work_min = preset['workDuration'] // 60
            break_min = preset['breakDuration'] // 60
            
            print(f"{i}. 🎯 {preset['name']}")
            print(f"   ⏱️  Упражнения: {work_min} мин | Отдых: {break_min} мин")
            print(f"   🔄 Циклов: {preset['cycles']}")
            print(f"   📝 {preset['description']}")
            
            if preset['id'] == 'quick_test':
                print(f"   🧪 [ТЕСТОВЫЙ РЕЖИМ - для проверки]")
            print()
    
    def create_timer(self, preset_id):
        """Создание таймера по ID пресета"""
        preset = next((p for p in self.presets if p['id'] == preset_id), None)
        
        if preset:
            timer = PomodoroTimer(
                work_duration=preset['workDuration'],
                break_duration=preset['breakDuration'],
                cycles=preset['cycles'],
                name=preset['name']
            )
            return timer
        else:
            print(f"❌ Режим с ID '{preset_id}' не найден")
            return None
    
    def start_timer_by_id(self, preset_id):
        """Запуск таймера по ID пресета"""
        if self.current_timer and self.current_timer.is_running:
            print("❌ Уже запущен другой таймер. Сначала остановите его.")
            return
        
        self.current_timer = self.create_timer(preset_id)
        if self.current_timer:
            self.current_timer.start()
            return True
        return False
    
    def start_timer_by_index(self, index):
        """Запуск таймера по номеру в списке"""
        if 1 <= index <= len(self.presets):
            preset_id = self.presets[index-1]['id']
            return self.start_timer_by_id(preset_id)
        else:
            print("❌ Неверный номер режима")
            return False
    
    def stop_current_timer(self):
        """Остановка текущего таймера"""
        if self.current_timer:
            self.current_timer.stop()
            self.current_timer = None
            print("✅ Таймер остановлен")
        else:
            print("❌ Нет активного таймера")
    
    def get_current_status(self):
        """Получение статуса текущего таймера"""
        if self.current_timer:
            return self.current_timer.get_status()
        return None
    
    def display_current_status(self):
        """Отображение статуса текущего таймера"""
        status = self.get_current_status()
        if status:
            print(f"\n📊 ТЕКУЩИЙ СТАТУС:")
            print(f"   🎯 Режим: {status['name']}")
            print(f"   🔄 Цикл: {status['progress']}")
            print(f"   📝 Статус: {'Запущен' if status['is_running'] else 'Остановлен'}")
            if status['is_running']:
                mode_emoji = "💪" if status['current_mode'] == 'work' else "☕"
                print(f"   ⏰ Фаза: {mode_emoji} {status['current_mode'].upper()}")
        else:
            print("❌ Нет активного таймера")
