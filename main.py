COLUNAS  = ("a", "b", "c")
LINHAS   = ("1", "2", "3")
DUPLO_VENCEDOR = "_"


# ======== TAD POSICAO ======== #
"""
    O TAD posicao consiste numa string com 2 caracteres,
    uma letra correspondente a coluna seguida de um numero 
    que representa a linha
"""


def cria_posicao(c, l):
    if c in COLUNAS and l in LINHAS:
        return c.lower() + l.lower()
    else:
        raise ValueError("cria_posicao: argumentos invalidos")


CANTOS   = (cria_posicao("a", "1"), cria_posicao("c", "1"), cria_posicao("a", "3"), cria_posicao("c", "3"))
LATERAIS = (cria_posicao("b", "1"), cria_posicao("a", "2"), cria_posicao("c", "2"), cria_posicao("b", "3"))
CENTRO   = cria_posicao("b", "2")


"""
    str e imutavel, devolve o argumento
"""
def cria_copia_posicao(pos):
    return pos


def obter_pos_c(pos):
    if eh_posicao(pos):
        return pos[0]


def obter_pos_l(pos):
    if eh_posicao(pos):
        return pos[1]


def eh_posicao(arg):
    return (type(arg) is str and
            len(arg) == 2 and
            arg[0] in COLUNAS and
            arg[1] in LINHAS)


def posicoes_iguais(pos1, pos2):
    return (eh_posicao(pos1) and
            eh_posicao(pos2) and
            obter_pos_c(pos1) == obter_pos_c(pos2) and
            obter_pos_l(pos1) == obter_pos_l(pos2))


def posicao_para_str(pos):
    return pos


def obter_linhas_adjacentes(pos):
    if obter_pos_l(pos) == "2":
        return "1", "3"
    else:
        return "2",


def obter_colunas_adjacentes(pos):
    if obter_pos_c(pos) == "b":
        return "a", "c"
    else:
        return "b",


def obter_diagonais_adjacentes(pos):
    if pos in CANTOS:
        return CENTRO,
    elif pos == CENTRO:
        return CANTOS
    else:
        return ()


def obter_posicoes_adjacentes(pos):
    adj = ()
    for l in obter_linhas_adjacentes(pos):
        adj += (cria_posicao(obter_pos_c(pos), l),)
    for c in obter_colunas_adjacentes(pos):
        adj += (cria_posicao(c, obter_pos_l(pos)),)
    adj += obter_diagonais_adjacentes(pos)
    return ordenar_vec(adj)


def obter_posicoes_adjacentes_livres(tab, pos):
    return tuple(p for p in obter_posicoes_adjacentes(pos) if eh_posicao_livre(tab, p))


def ordenar_vec(vec):
    sort = ()
    vec = list(vec)
    while len(vec) > 0:
        mnm = vec[0]
        for e in vec:
            if (obter_pos_l(e) < obter_pos_l(mnm) or
                    obter_pos_l(e) == obter_pos_l(mnm) and
                    obter_pos_c(e) < obter_pos_c(mnm)):
                mnm = e
        sort += mnm,
        vec.remove(mnm)
    return sort


# ======== TAD PECA ======== #


def cria_peca(s):
    if s in ("O", " ", "X"):
        return s
    else:
        raise ValueError("cria_peca: argumento invalido")


PECA_VAZIA = cria_peca(" ")
PECA_X     = cria_peca("X")
PECA_O     = cria_peca("O")
PECAS = (PECA_O, PECA_VAZIA, PECA_X)


def cria_copia_peca(pec):
    return pec


def eh_peca(arg):
    return type(arg) is str and arg in PECAS


def pecas_iguais(pec1, pec2):
    return (eh_peca(pec1) and
            eh_peca(pec2) and
            pec1 == pec2)


def peca_para_str(pec):
    return "[" + pec + "]"


def peca_para_inteiro(pec):
    return "O X".index(pec) - 1


def peca_oposta(pec):
    return {PECA_O: PECA_X, PECA_X: PECA_O}.get(pec)


# ======== TAD TABULEIRO ======== #


def cria_tabuleiro():
    tab = {}
    for l in LINHAS:
        for c in COLUNAS:
            coloca_peca(tab, PECA_VAZIA, cria_posicao(c, l))
    return tab


def cria_copia_tabuleiro(tab):
    return dict(tab)


def obter_peca(tab, pos):
    return tab.get(pos)


def obter_vetor(tab, s):
    srt = ()
    for pos in tab:
        if (s in LINHAS and obter_pos_l(pos) == s or
                s in COLUNAS and obter_pos_c(pos) == s):
            srt += pos,
    srt = ordenar_vec(srt)
    vec = ()
    for v in srt:
        vec += obter_peca(tab, v),
    return vec


def coloca_peca(tab, pec, pos):
    tab[pos] = pec
    return tab


def remove_peca(tab, pos):
    tab[pos] = " "
    return tab


def move_peca(tab, posi, posf):
    coloca_peca(tab, obter_peca(tab, posi), posf)
    remove_peca(tab, posi)
    return tab


def eh_tabuleiro(arg):
    if type(arg) is dict and len(arg) == 9:
        for key in arg:
            if not (eh_posicao(key) and arg.get(key) in PECAS):
                return False
        n_pecas_x, n_pecas_o = len(obter_posicoes(arg, PECA_X)), len(obter_posicoes(arg, PECA_O))
        if (abs(n_pecas_x - n_pecas_o) > 1 or
                n_pecas_x > 3 or n_pecas_o > 3 or
                obter_ganhador(arg) == DUPLO_VENCEDOR):
            return False
        return True
    else:
        return False


def eh_posicao_livre(tab, pos):
    return obter_peca(tab, pos) == PECA_VAZIA


def tabuleiros_iguais(tab1, tab2):
    return (eh_tabuleiro(tab1) and
            eh_tabuleiro(tab2) and
            tab1 == tab2)


def tabuleiro_para_str(tab):
    return "   a   b   c\n1 [{}]-[{}]-[{}]\n   | \\ | / |\n2 [{}]-[{}]-[{}]\n   | / | \\ |\n3 [{}]-[{}]-[{}]"\
        .format(obter_peca(tab, "a1"), obter_peca(tab, "b1"), obter_peca(tab, "c1"),
                obter_peca(tab, "a2"), obter_peca(tab, "b2"), obter_peca(tab, "c2"),
                obter_peca(tab, "a3"), obter_peca(tab, "b3"), obter_peca(tab, "c3"))


def tuplo_para_tabuleiro(tup):
    tab = {}
    for l in LINHAS:
        for c in COLUNAS:
            tab[cria_posicao(c, l)] = PECAS[tup[int(l) - 1][COLUNAS.index(c)] + 1]
    return tab


def vec_ganhador(vec):
    return vec[0] == vec[1] == vec[2] != PECA_VAZIA


def obter_ganhador(tab):
    win = PECA_VAZIA
    for l in LINHAS:
        vec = obter_vetor(tab, l)
        if vec_ganhador(vec):
            if win != PECA_VAZIA:
                return DUPLO_VENCEDOR
            win = vec[0]
    for c in COLUNAS:
        vec = obter_vetor(tab, c)
        if vec_ganhador(vec):
            if win != PECA_VAZIA:
                return DUPLO_VENCEDOR
            win = vec[0]

    return win


def obter_posicoes(tab, pec):
    vec = ()
    for l in LINHAS:
        for c in COLUNAS:
            pos = cria_posicao(c, l)
            if obter_peca(tab, pos) == pec:
                vec += pos,
    return vec


def obter_posicoes_livres(tab):
    return obter_posicoes(tab, PECA_VAZIA)


def obter_posicoes_jogador(tab, pec):
    return obter_posicoes(tab, pec)


# ======== FUNCOES ADICIONAIS ======== #


def obter_movimento_manual(tab, pec):
    if len(obter_posicoes_livres(tab)) == 3:
        jogada = input("Turno do jogador. Escolha um movimento: ")
        if len(jogada) == 4:
            posi, posf = cria_posicao(jogada[0], jogada[1]), cria_posicao(jogada[2], jogada[3])
            if (eh_posicao(posi) and eh_posicao(posf) and
                    (posf in obter_posicoes_adjacentes_livres(tab, posi) or posi == posf)):
                peci, pecf = obter_peca(tab, posi), obter_peca(tab, posf)
                if (pec == peci == pecf or
                        pec == peci and pecf == PECA_VAZIA):
                    return posi, posf
    else:
        jogada = input("Turno do jogador. Escolha uma posicao: ")
        if len(jogada) == 2:
            pos = cria_posicao(jogada[0], jogada[1])
            if eh_posicao(jogada):
                if eh_posicao_livre(tab, pos):
                    return pos,
    raise ValueError("obter_movimento_manual: escolha invalida")


def obter_movimento_auto(tab, pec, dif):
    if len(obter_posicoes_livres(tab)) == 3:
        if dif == "facil":
            return obter_movimento_auto_facil(tab, pec)
        elif dif == "normal":
            return obter_movimento_auto_normal(tab, pec)
        elif dif == "dificil":
            return obter_movimento_auto_dificil(tab, pec)
    else:
        crtrs = (crit_vitoria(tab, pec),
                 crit_bloqueio(tab, pec),
                 crit_centro(tab),
                 crit_canto_vazio(tab),
                 crit_lateral_vazio(tab))
        for c in crtrs:
            if c is not None:
                return c,


def crit_vitoria(tab, pec):
    for l in LINHAS:
        for c in COLUNAS:
            pos = cria_posicao(c, l)
            if obter_ganhador(coloca_peca(cria_copia_tabuleiro(tab), pec, pos)) == pec:
                return pos


def crit_bloqueio(tab, pec):
    return crit_vitoria(tab, peca_oposta(pec))


def crit_centro(tab):
    return CENTRO if eh_posicao_livre(tab, CENTRO) else None


def crit_canto_vazio(tab):
    for p in CANTOS:
        if eh_posicao_livre(tab, p):
            return p


def crit_lateral_vazio(tab):
    for p in LATERAIS:
        if eh_posicao_livre(tab, p):
            return p


def obter_movimento_auto_facil(tab, pec):
    for pos in obter_posicoes(tab, pec):
        liv = obter_posicoes_adjacentes_livres(tab, pos)
        if len(liv) > 0:
            return pos, liv[0]


def valor_tabuleiro(tab):
    win = obter_ganhador(tab)
    return 1 if win == PECA_X else (-1 if win == PECA_O else 0)


def minimax(tab, jog, depth, seq=()):
    if obter_ganhador(tab) != PECA_VAZIA or depth == 0:
        return valor_tabuleiro(tab), seq
    else:
        melhor_res = PECAS.index(peca_oposta(jog)) - 1
        for pos in obter_posicoes(tab, jog):
            for adj in obter_posicoes_adjacentes_livres(tab, pos):
                novo_tab = move_peca(cria_copia_tabuleiro(tab), pos, adj)
                novo_res, nova_seq = minimax(novo_tab, peca_oposta(jog), depth - 1, seq + ((pos, adj),))
                if ("melhor_seq" not in locals() or
                        jog == PECA_X and novo_res > melhor_res or
                        jog == PECA_O and novo_res < melhor_res):
                    melhor_res, melhor_seq = novo_res, nova_seq
        if "melhor_seq" in locals():
            return melhor_res, melhor_seq
        else:
            return melhor_res, seq


def obter_movimento_auto_normal(tab, pec):
    return minimax(tab, pec, 1)[1][0]


def obter_movimento_auto_dificil(tab, pec):
    return minimax(tab, pec, 5)[1][0]


def moinho(jog, dif):
    jogs = (peca_para_str(PECA_O), peca_para_str(PECA_X))
    difs = ("facil", "normal", "dificil")
    if jog in jogs and dif in difs:
        jog = cria_peca(jog[1])
        turno = cria_peca("X")
        tab = cria_tabuleiro()
        print("Bem-vindo ao JOGO DO MOINHO. Nivel de dificuldade {}.".format(dif))

        while True:
            print(tabuleiro_para_str(tab))
            if obter_ganhador(tab) != PECA_VAZIA:
                win = peca_para_str(obter_ganhador(tab))
                break

            if jog == turno:
                jogada = obter_movimento_manual(tab, jog)
            else:
                print("Turno do computador ({}):".format(dif))
                jogada = obter_movimento_auto(tab, turno, dif)

            if len(jogada) == 1:
                coloca_peca(tab, turno, jogada[0])
            else:
                move_peca(tab, jogada[0], jogada[1])

            turno = peca_oposta(turno)

        return win
    else:
        raise ValueError("moinho: argumentos invalidos")
