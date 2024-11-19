import random
import time
import os
import sys
import threading
import textwrap

class CyberpunkPuzzle:
    def __init__(self):
        # Configurações do jogo
        self.max_attempts = 3  # Reduzido para 3 tentativas
        self.target_code = self.generate_complex_code()
        self.attempts = 0
        self.difficulty_multiplier = 1.5
        self.code_revealed = False
        
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
            
            # Se o maior dado for 5, mostra 4 códigos aleatórios
            if max_dado == 5:
                self.play_sound('success')
                self.typing_effect(">>> CÓDIGOS DETECTADOS <<<", delay=0.05, color="\033[92m")
                
                fake_codes = self.generate_fake_codes()
                print("\033[93mCÓDIGOS ENCONTRADOS:\033[0m")
                for i, code in enumerate(fake_codes, 1):
                    print(f"{i}. {code}")
                
                return True
            # Se o maior dado for 6, revela o código correto
            elif max_dado == 6:
                self.play_sound('success')
                self.code_revealed = True
                self.typing_effect(">>> CÓDIGO CORRETO REVELADO <<<", delay=0.05, color="\033[92m")
                print(f"\033[92mCódigo correto: {self.target_code}\033[0m")
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
    
    def start_puzzle(self):
        """Inicia o puzzle cyberpunk"""
        self.play_sound('startup')
        self.reset_game_state()  # Nova função para resetar o estado do jogo
        
        while self.attempts < self.max_attempts:
            self.clear_screen()  # Limpa a tela no início de cada iteração
            self.cyberpunk_header()
            
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
        - SEGURANÇA NEURAL BYPASSED
        - NIVEL DE SUCESSO: MÁXIMO
        """)
        self.typing_effect(vitoria_msg, delay=0.03, color="\033[96m")
        
        self.glitch_effect(5)
    
    def defeat(self):
        """Sequência de derrota com tela de firewall"""
        self.play_sound('failure')
        self.clear_screen()
        
        firewall_screen = textwrap.dedent(f"""
        ██████████████████████████████████████████
        █ SISTEMA DE SEGURANÇA NEURAL - FIREWALL █
        ██████████████████████████████████████████
        
        >>> INTRUSÃO DETECTADA <<<
        
        STATUS: INVASÃO BLOQUEADA
        ORIGEM DA TENTATIVA: [ENDEREÇO IP CENSURADO]
        NIVEL DE AMEAÇA: CRÍTICO
        CÓDIGO CORRETO ERA: {self.target_code}
        
        AÇÕES AUTOMÁTICAS:
        - RASTREAMENTO DE ORIGEM INICIADO
        - PROTOCOLO DE CONTRA-ATAQUE ATIVADO
        - REGISTRO DE INVASÃO ARQUIVADO
        
        MENSAGEM DO SISTEMA:
        SUA TENTATIVA DE INVASÃO FOI REGISTRADA 
        E SERÁ PROCESSADA PELAS AUTORIDADES DIGITAIS.
        
        FIREWALL STATUS: 🔒 BLOQUEIO TOTAL 🔒
        """)
        
        print("\033[91m")
        for line in firewall_screen.split('\n'):
            self.typing_effect(line, delay=0.02, color="\033[91m")
            time.sleep(0.1)
        print("\033[0m")
        
        self.glitch_effect(10)
        time.sleep(1)
        self.typing_effect(">>> INVASÃO NEUTRALIZADA <<<", delay=0.05, color="\033[91m")

def main():
    while True:
        puzzle = CyberpunkPuzzle()
        puzzle.start_puzzle()
        
        rejogar = input("\033[97m>> REINICIAR PROTOCOLO? (S/N): \033[0m").strip().upper()
        if rejogar != 'S':
            puzzle.typing_effect(">>> ENCERRANDO SISTEMA NEURAL <<<", delay=0.05, color="\033[94m")
            break

if __name__ == "__main__":
    try:
        import playsound
    except ImportError:
        print("Instalando dependências necessárias...")
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'playsound'])
    
    if not os.path.exists('sons'):
        os.mkdir('sons')
        print("AVISO: Pasta 'sons' criada. Adicione os arquivos de som:")
        print("- startup.wav")
        print("- typing.wav")
        print("- error.wav")
        print("- success.wav")
        print("- failure.wav")
    
    main()