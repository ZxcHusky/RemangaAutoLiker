from remanga import Remanga
import time
import random

class RemangaAutoLiker:
    def __init__(self, login: str, password: str):
        self.client = Remanga()
        self.login = login
        self.password = password
        
    def auth(self) -> bool:
        """Авторизация на сайте"""
        try:
            auth_result = self.client.login(self.login, self.password)
            
            if hasattr(self.client, 'access_token') and self.client.access_token:
                print("Успешная авторизация")
                return True
            else:
                print(f"Ошибка авторизации. Ответ: {auth_result}")
                return False
        except Exception as e:
            print(f"Ошибка при авторизации: {e}")
            return False
    
    def process_title(self, title_url: str, delay: tuple = (3, 7)):
        """Обработка тайтла"""
        try:
            parts = title_url.split('/')
            dir_name = parts[-2] if parts[-1] == "main" else parts[-1]
            
            title_info = self.client.get_title_info(dir_name)
            if not title_info or "content" not in title_info:
                print("Тайтл не найден")
                return False
            
            title_data = title_info["content"]
            manga_name = title_data.get("rus_name", dir_name)
            branches = title_data.get("branches", [])
            
            if not branches:
                print("Нет доступных веток")
                return False
                
            print(f"\nОбработка тайтла: {manga_name}")
            branch_id = branches[0]["id"]
            
            chapters = self.client.get_all_chapters(branch_id)
            if not chapters:
                print("Нет глав для обработки")
                return False
                
            print(f"Всего глав: {len(chapters)}")
            
            success = 0
            for i, chapter in enumerate(chapters, 1):
                try:
                    chapter_id = chapter["id"]
                    chapter_name = chapter.get("name", f"Глава {chapter.get('chapter', 'N/A')}")
                    
                    like_response = self.client.like_chapter(chapter_id)
                    
                    if isinstance(like_response, dict) and like_response.get("error"):
                        print(f"[{i}/{len(chapters)}] Ошибка: {like_response.get('message')}")
                    else:
                        print(f"[{i}/{len(chapters)}] Лайк: {chapter_name}")
                        success += 1
                    
                    time.sleep(random.uniform(*delay))
                    
                except Exception as e:
                    print(f"[{i}/{len(chapters)}] Ошибка главы: {e}")
                    continue
                    
            print(f"\nУспешно: {success}/{len(chapters)} глав")
            return True
            
        except Exception as e:
            print(f"Ошибка обработки: {e}")
            return False

if __name__ == "__main__":
    LOGIN = "Zxcurcedxxx"
    PASSWORD = "Moskow10"
    TITLE_URL = "https://remanga.org/manga/i-am-a-fulltime-newbie-exclusive/main"  # С /main
    
    bot = RemangaAutoLiker(LOGIN, PASSWORD)
    if bot.auth():
        bot.process_title(TITLE_URL)
    else:
        print("Ошибка авторизации")