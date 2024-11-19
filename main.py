import random
import time
import os
import sys
import threading
import textwrap

class CyberpunkPuzzle:
    def __init__(self):
        # Configurações do jogo
        self.max_attempts = 3
        self.target_code = self.generate_complex_code()
        self.attempts = 0
        self.difficulty_multiplier = 1.5
        self.code_revealed = False
        self.displayed_codes = []  # Lista para armazenar códigos revelados
        
        # Sons
        self.sounds = {
            'startup': 'sons/startup.wav',
            'typing': 'sons/typing.wav',
            'error': 'sons/error.wav',
            'success': 'sons/success.wav',
            'failure': 'sons/failure.wav'
        }
    
    def generate_complex_code(self):
        """Gera um código mais complexo"""
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        code = ''.join([
            random.choice(letters) for _ in range(3)
        ]) + ''.join([
            str(random.randint(0, 9)) for _ in range(3)
        ])
        return code
    
    def generate_fake_codes(self):
        """Gera 4 códigos aleatórios diferentes"""
        codes = []
        while len(codes) < 4:
            new_code = self.generate_complex_code()
            if new_code not in codes:  # Garante que não há códigos duplicados
                codes.append(new_code)
        return codes
    
    def play_sound(self, sound_type):
        """Reproduz efeito sonoro em thread separada"""
        try:
            def play():
                try:
                    playsound.playsound(self.sounds[sound_type])
                except Exception as e:
                    print(f"Erro ao reproduzir som: {e}")
            
            sound_thread = threading.Thread(target=play)
            sound_thread.start()
        except Exception as e:
            print(f"Erro ao iniciar thread de som: {e}")
    
    def typing_effect(self, text, delay=0.05, color="\033[92m"):
        """Simula efeito de digitação"""
        self.play_sound('typing')
        sys.stdout.write(color)
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        sys.stdout.write("\033[0m\n")
    
    def glitch_effect(self, intensity=3):
        """Cria efeito de glitch no console"""
        glitch_messages = [
            "ERRO DE SISTEMA: FIREWALL ATIVADO",
            "PROTEÇÃO NEURAL INTERFERINDO",
            "CONEXÃO INSTÁVEL",
            "DECRYPT.EXE BLOQUEADO"
        ]
        
        for _ in range(intensity):
            glitch_msg = random.choice(glitch_messages)
            print("\033[91m" + glitch_msg.center(50) + "\033[0m")
            time.sleep(0.2)
    
    def roll_skill_test(self):
        """Realiza teste de perícia para revelar código"""
        try:
            self.play_sound('typing')
            dados = int(input("\n\033[97m>> Quantos dados de 6 lados deseja rolar? \033[0m"))
            resultados = [random.randint(1, 6) for _ in range(dados)]
            
            print("\033[96mResultados dos dados:\033[0m", resultados)
            
            # Encontra o maior número nos dados
            max_dado = max(resultados) if resultados else 0
            
            if max_dado == 5:
                self.play_sound('success')
                fake_codes = self.generate_fake_codes()
                self.displayed_codes.extend(fake_codes)
                self.typing_effect(">>> CÓDIGOS DETECTADOS <<<", delay=0.05, color="\033[92m")
                self.show_codes()
                return True
            
            elif max_dado == 6:
                self.play_sound('success')
                self.code_revealed = True
                self.typing_effect(">>> CÓDIGO CORRETO REVELADO <<<", delay=0.05, color="\033[92m")
                print(f"\033[92mCódigo correto: {self.target_code}\033[0m")
                self.displayed_codes.append(self.target_code)
                return True
            
            else:
                self.attempts += 1
                self.play_sound('error')
                self.glitch_effect()
                self.typing_effect(f">>> TESTE DE PERÍCIA FALHOU <<< [{self.max_attempts - self.attempts} TENTATIVAS RESTANTES]", 
                                 delay=0.05, color="\033[91m")
                
                if self.attempts >= self.max_attempts:
                    self.defeat()
                    return False
                    
                return False
        except ValueError:
            self.typing_effect("Entrada inválida. Use um número inteiro.", delay=0.05, color="\033[91m")
            return False
    
    def show_codes(self):
        """Mostra os códigos na página inicial"""
        print("\033[93mCÓDIGOS ENCONTRADOS ATÉ AGORA:\033[0m")
        for code in self.displayed_codes:
            print(f"- {code}")
    
    def start_puzzle(self):
        """Inicia o puzzle cyberpunk"""
        self.play_sound('startup')
        self.reset_game_state()
        
        while self.attempts < self.max_attempts:
            self.clear_screen()
            self.cyberpunk_header()
            self.show_codes()  # Mantém os códigos visíveis na tela inicial
            
            self.typing_effect("INICIANDO PROTOCOLO DE QUEBRA-CABEÇA NEURAL", delay=0.05, color="\033[94m")
            time.sleep(0.5)
            
            descricao_regras = textwrap.dedent(f"""
            PARAMETROS DO SISTEMA:
            - TENTATIVAS MÁXIMAS: {self.max_attempts}
            - COMPLEXIDADE: NIVEL ULTRA
            - TENTATIVAS RESTANTES: {self.max_attempts - self.attempts}
            """)
            self.typing_effect(descricao_regras, delay=0.03, color="\033[96m")
            
            opcoes = """
            OPÇÕES:
            1. ROLAR TESTE DE PERÍCIA
            2. TENTAR DECIFRAR CÓDIGO
            """
            print("\033[93m" + opcoes + "\033[0m")
            
            try:
                escolha = input("\n\033[97m>> SELECIONE UMA OPÇÃO (1/2): \033[0m").strip()
                
                if escolha == '1':
                    if not self.roll_skill_test() and self.attempts >= self.max_attempts:
                        return
                elif escolha == '2':
                    tentativa = input("\n\033[97m>> INSIRA CÓDIGO DE ACESSO: \033[0m").upper().strip()
                    self.attempts += 1
                    
                    if tentativa == self.target_code:
                        self.victory()
                        return
                    else:
                        self.play_sound('error')
                        self.glitch_effect()
                        erro_msgs = [
                            f"DECRYPT FALHOU. CÓDIGO INCORRETO. [{self.max_attempts - self.attempts} TENTATIVAS]",
                            f"ACESSO NEGADO. PADRÃO NÃO RECONHECIDO. [{self.max_attempts - self.attempts} RESTANTES]"
                        ]
                        self.typing_effect(random.choice(erro_msgs), delay=0.05, color="\033[91m")
                else:
                    self.typing_effect("OPÇÃO INVÁLIDA. SELECIONE 1 OU 2.", delay=0.05, color="\033[91m")
            
            except Exception as e:
                self.typing_effect(f"ERRO CRÍTICO: {str(e)}", delay=0.05, color="\033[91m")
            
            if self.attempts >= self.max_attempts:
                self.defeat()
                return
    
    def reset_game_state(self):
        """Reseta o estado do jogo para uma nova partida"""
        self.target_code = self.generate_complex_code()
        self.attempts = 0
        self.code_revealed = False
        self.displayed_codes = []
    
    def clear_screen(self):
        """Limpa a tela do console"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def cyberpunk_header(self):
        """Cabeçalho estilizado de console cyberpunk"""
        header_text = ">>> SISTEMA DE SEGURANÇA NEURAL v1.2.5 <<<"
        print("\033[91m" + "=" * 50)
        print(header_text.center(50))
        print("=" * 50 + "\033[0m")
    
    def victory(self):
        """Sequência de vitória"""
        self.play_sound('success')
        self.clear_screen()
        self.cyberpunk_header()
        self.typing_effect(">>> ACESSO CONCEDIDO <<<", delay=0.05, color="\033[92m")
        time.sleep(0.5)
        vitoria_msg = textwrap.dedent(f"""
        RELATÓRIO DE OPERAÇÃO:
        - CÓDIGO DECIFRADO EM {self.attempts} TENTATIVAS
        - SEGURANÇA DE SISTEMA COMPROMETIDA
        """)
        self.typing_effect(vitoria_msg, delay=0.05, color="\033[96m")
    
    def defeat(self):
        """Sequência de derrota"""
        self.play_sound('failure')
        self.clear_screen()
        self.cyberpunk_header()
        self.typing_effect(">>> ACESSO NEGADO <<<", delay=0.05, color="\033[91m")
        self.typing_effect(">>> TENTATIVAS EXCEDIDAS <<<", delay=0.05, color="\033[91m")
        time.sleep(1)
        derrota_msg = textwrap.dedent(f"""
        RELATÓRIO DE OPERAÇÃO:
        - OPERAÇÃO FALHOU
        - SEGURANÇA NEURAL ATIVADA
        """)
        self.typing_effect(derrota_msg, delay=0.05, color="\033[96m")

# Inicia o jogo
if __name__ == "__main__":
    CyberpunkPuzzle().start_puzzle()
