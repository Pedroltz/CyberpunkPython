import random
import time
import os
import sys
import threading
import textwrap

class CyberpunkPuzzle:
    def __init__(self):
        # Configurações do jogo
        self.max_attempts = 5
        self.target_code = self.generate_complex_code()
        self.attempts = 0
        self.difficulty_multiplier = 1.5
        self.code_revealed = False
        self.alternate_codes = self.generate_alternate_codes()
        
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
    
    def generate_alternate_codes(self):
        """Gera códigos alternativos para escolha"""
        alt_codes = [self.target_code]
        while len(alt_codes) < 2:
            alternate = self.generate_complex_code()
            if alternate != self.target_code and alternate not in alt_codes:
                alt_codes.append(alternate)
        return alt_codes
    
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
            
            # Se o maior dado for 5, revela dois códigos
            if max_dado == 5:
                self.play_sound('success')
                self.code_revealed = True
                self.typing_effect(">>> CÓDIGOS REVELADOS <<<", delay=0.05, color="\033[92m")
                
                # Mostra os dois códigos gerados
                print("\033[93mCÓDIGOS DISPONÍVEIS:\033[0m")
                for i, code in enumerate(self.alternate_codes, 1):
                    print(f"{i}. {code}")
                
                return True
            # Se o maior dado for menor que 5, falha automaticamente
            elif max_dado < 5:
                self.play_sound('error')
                self.glitch_effect()
                self.typing_effect(">>> TESTE DE PERÍCIA FALHOU <<<", delay=0.05, color="\033[91m")
                return False
            # Se o maior dado for 6, permite tentativa normal
            else:
                self.play_sound('success')
                self.code_revealed = True
                self.typing_effect(">>> CÓDIGO REVELADO <<<", delay=0.05, color="\033[92m")
                return True
        except ValueError:
            self.typing_effect("Entrada inválida. Use um número inteiro.", delay=0.05, color="\033[91m")
            return False
    
    def start_puzzle(self):
        """Inicia o puzzle cyberpunk"""
        self.play_sound('startup')
        self.clear_screen()
        self.cyberpunk_header()
        
        self.typing_effect("INICIANDO PROTOCOLO DE QUEBRA-CABEÇA NEURAL", delay=0.05, color="\033[94m")
        time.sleep(0.5)
        
        while self.attempts < self.max_attempts:
            # Mostra código como **** se não revelado
            display_code = self.target_code if self.code_revealed else '*' * len(self.target_code)
            
            descricao_regras = textwrap.dedent(f"""
            PARAMETROS DO SISTEMA:
            - DECIFRAR CÓDIGO NEURAL: {display_code}
            - TENTATIVAS MÁXIMAS: {self.max_attempts}
            - COMPLEXIDADE: NIVEL ULTRA
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
                    test_result = self.roll_skill_test()
                elif escolha == '2':
                    # Só permite tentar decifrar se o código foi revelado
                    if not self.code_revealed:
                        self.play_sound('error')
                        self.typing_effect("CÓDIGO AINDA NÃO REVELADO. REALIZE O TESTE DE PERÍCIA PRIMEIRO.", delay=0.05, color="\033[91m")
                        continue
                    
                    tentativa = input("\n\033[97m>> INSIRA CÓDIGO DE ACESSO: \033[0m").upper().strip()
                    self.attempts += 1
                    
                    # Se o código for igual a qualquer um dos códigos revelados, permite acesso
                    if tentativa in self.alternate_codes:
                        if tentativa == self.target_code:
                            self.victory()
                        else:
                            # Se o código não for o verdadeiro, chama a tela de derrota
                            self.defeat()
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
        
        self.defeat()
    
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
        
        # Tela de interceptação do firewall
        firewall_screen = textwrap.dedent("""
        ██████████████████████████████████████████
        █ SISTEMA DE SEGURANÇA NEURAL - FIREWALL █
        ██████████████████████████████████████████
        
        >>> INTRUSÃO DETECTADA <<<
        
        STATUS: INVASÃO BLOQUEADA
        ORIGEM DA TENTATIVA: [ENDEREÇO IP CENSURADO]
        NIVEL DE AMEAÇA: CRÍTICO
        
        AÇÕES AUTOMÁTICAS:
        - RASTREAMENTO DE ORIGEM INICIADO
        - PROTOCOLO DE CONTRA-ATAQUE ATIVADO
        - REGISTRO DE INVASÃO ARQUIVADO
        
        MENSAGEM DO SISTEMA:
        SUA TENTATIVA DE INVASÃO FOI REGISTRADA 
        E SERÁ PROCESSADA PELAS AUTORIDADES DIGITAIS.
        
        FIREWALL STATUS: 🔒 BLOQUEIO TOTAL 🔒
        """)
        
        # Efeito de digitação na tela de firewall
        print("\033[91m")
        for line in firewall_screen.split('\n'):
            self.typing_effect(line, delay=0.02, color="\033[91m")
            time.sleep(0.1)
        print("\033[0m")
        
        # Efeitos adicionais
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