#!/usr/bin/env python3
import os
import sys
from pomodoro_manager import PomodoroManager

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_welcome():
    clear_screen()
    print("🌟" * 30)
    print("🎯          POMODORO ТАЙМЕР ДЛЯ УТРЕННЕЙ ЗАРЯДКИ          🎯")
    print("🌟" * 30)
    print()

def main():
    manager = PomodoroManager("config.json")
    
    while True:
        display_welcome()
        print("📝 ГЛАВНОЕ МЕНЮ:")
        print("1. 🎯 Показать все режимы тренировки")
        print("2. 📖 Показать упражнения классического режима")
        print("3. 🚀 Запустить классический режим (20/5)")
        print("4. ⚡ Запустить экспресс-зарядку (10/2)") 
        print("5. 🧪 Запустить тестовый режим (10сек/5сек)")
        print("6. 🛑 Остановить текущий таймер")
        print("7. ❌ Выйти из программы")
        print()
        
        try:
            choice = input("Выберите действие (1-7): ").strip()
            
            if choice == "1":
                clear_screen()
                manager.list_presets()
                input("\n↵ Нажмите Enter для возврата в меню...")
            elif choice == "2":
                clear_screen()
                manager.show_exercise_details("classic_20_5")
                input("\n↵ Нажмите Enter для возврата в меню...")
            elif choice == "3":
                clear_screen()
                print("🚀 Запуск Классического режима...")
                if manager.start_timer_by_id("classic_20_5"):
                    input("\n↵ Нажмите Enter когда закончите...")
                    manager.stop_current_timer()
            elif choice == "4":
                clear_screen()
                print("⚡ Запуск Экспресс-зарядки...")
                if manager.start_timer_by_id("express_10_2"):
                    input("\n↵ Нажмите Enter когда закончите...")
                    manager.stop_current_timer()
            elif choice == "5":
                clear_screen()
                print("🧪 Запуск Тестового режима...")
                if manager.start_timer_by_id("quick_test"):
                    input("\n↵ Нажмите Enter когда закончите...")
                    manager.stop_current_timer()
            elif choice == "6":
                manager.stop_current_timer()
                input("\n↵ Нажмите Enter для продолжения...")
            elif choice == "7":
                manager.stop_current_timer()
                print("\n👋 До свидания! Хорошего дня! 💪")
                break
            else:
                print("❌ Неверный выбор.")
                input("\n↵ Нажмите Enter для продолжения...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Выход из программы...")
            manager.stop_current_timer()
            break

if __name__ == "__main__":
    main()
