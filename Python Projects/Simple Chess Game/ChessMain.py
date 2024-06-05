import pygame as p
import ChessEngine
import ChessBot
import config

p.init()

BOARD_WIDTH = BOARD_HEIGHT = config.BOARD_WIDTH
MOVE_LOG_PANNEL_WIDTH = config.MOVE_LOG_PANNEL_WIDTH
MOVE_LOG_PANNEL_HEIGHT = config.MOVE_LOG_PANNEL_HEIGHT
DIMENTION = config.DIMENSION
SQ_SIZE = BOARD_HEIGHT // DIMENTION
MAX_FPS = config.MAX_FPS
IMAGES = {}
MOVE_LOG_FONT = p.font.SysFont(config.MOVE_LOG_FONT_NAME, config.MOVE_LOG_FONT_SIZE, False, False)


def loadImages():
    pieces = ['bP', 'bR', 'bN', 'bB', 'bQ', 'bK', 'wP', 'wR', 'wN', 'wB', 'wQ', 'wK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(config.IMAGE_FOLDER + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def main():
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANNEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    loadImages()
    running = True
    animate = False
    sqSelected = ()
    playerClicks = []
    playerOne = config.PLAYER_ONE_HUMAN
    playerTwo = config.PLAYER_TWO_HUMAN
    gameOver = False
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if not playerOne:
                        row, col = blackPerspectiveRow(row, col)
                    if (col >= 8) or col < 0:
                        continue
                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                        if len(playerClicks) == 2:
                            move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    gs.makeMove(validMoves[i])
                                    moveMade = True
                                    animate = True
                                    playerClicks = []
                                    sqSelected = ()
                            if not moveMade:
                                playerClicks = [sqSelected]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    gameOver = False
                    moveMade = True
                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
                    validMoves = gs.getValidMoves()

        if not gameOver and not humanTurn:
            AIMove = ChessBot.findBestMoveMinMax(gs, validMoves)
            if AIMove is None:
                AIMove = ChessBot.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True

        if moveMade:
            if len(gs.moveLog) > 0 and animate:
                animate = False
                animateMove(gs.moveLog[-1], screen, gs.board, clock, playerOne)
            validMoves = gs.getValidMoves()

            moveMade = False

        drawGameState(screen, gs, sqSelected, validMoves, playerOne)

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawEndGameText(screen, "Black Won by Checkmate!");
            else:
                drawEndGameText(screen, "White Won by Checkmate!");

        if gs.staleMate:
            gameOver = True
            drawEndGameText(screen, "Draw due to Stalemate!")

        clock.tick(MAX_FPS)
        p.display.flip()

def blackPerspectiveRow(r, c):
    return (7 - r, 7 - c)

def drawGameState(screen, gs, selectedSquare, validMoves, whitesPerspective):
    drawBoard(screen)
    highlightSquares(screen, gs, selectedSquare, validMoves, whitesPerspective)
    highlightCheck(screen, gs, whitesPerspective)
    if len(gs.moveLog) > 0:
        highlightLastMove(screen, gs.moveLog[-1], whitesPerspective)
    drawPieces(screen, gs.board, whitesPerspective)
    drawMoveLog(screen, gs)

def drawBoard(screen):
    global colors
    colors = [config.BOARD_COLOR_LIGHT, config.BOARD_COLOR_DARK]
    for r in range(DIMENTION):
        for c in range(DIMENTION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(SQ_SIZE * c, SQ_SIZE * r, SQ_SIZE, SQ_SIZE))

def highlightCheck(screen, gs, whitesPerspective):
    if gs.inCheck:
        r, c = gs.whiteKingLocation if gs.whiteToMove else gs.blackKingLocation
        if not whitesPerspective:
            r, c = blackPerspectiveRow(r, c)
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)
        s.fill(p.Color('red'))
        screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))

def highlightSquares(screen, gs, selectedSquare, validMoves, whitesPerspective):
    if selectedSquare != ():
        r, c = selectedSquare
        r1, c1 = r, c
        if not whitesPerspective:
            r1, c1 = blackPerspectiveRow(r, c)
        enemyColor = 'b' if gs.whiteToMove else 'w'
        allyColor = 'w' if gs.whiteToMove else 'b'
        if gs.board[r][c][0] == allyColor:
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (c1 * SQ_SIZE, r1 * SQ_SIZE))

            s.fill(p.Color('yellow'))

            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    endRow = move.endRow
                    endCol = move.endCol
                    drawEndRow, drawEndCol = endRow, endCol
                    if not whitesPerspective:
                        drawEndRow, drawEndCol = blackPerspectiveRow(endRow, endCol)
                    if gs.board[endRow][endCol] == '--' or gs.board[endRow][endCol][0] == enemyColor:
                        screen.blit(s, (drawEndCol * SQ_SIZE, drawEndRow * SQ_SIZE))

def highlightLastMove(screen, move, whitesPerspective):
    startRow = move.startRow
    startCol = move.startCol
    endRow = move.endRow
    endCol = move.endCol
    if not whitesPerspective:
        startRow, startCol = blackPerspectiveRow(startRow, startCol)
        endRow, endCol = blackPerspectiveRow(endRow, endCol)
    s = p.Surface((SQ_SIZE, SQ_SIZE))
    s.set_alpha(100)
    s.fill(p.Color("pink"))
    screen.blit(s, (startCol * SQ_SIZE, startRow * SQ_SIZE))
    screen.blit(s, (endCol * SQ_SIZE, endRow * SQ_SIZE))

def drawPieces(screen, board, whitesPerspective):
    for r in range(DIMENTION):
        for c in range(DIMENTION):
            r1, c1 = r, c
            if not whitesPerspective:
                r1, c1 = blackPerspectiveRow(r, c)
            piece = board[r1][c1]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(SQ_SIZE * c, SQ_SIZE * r, SQ_SIZE, SQ_SIZE))

def drawMoveLog(screen, gs):
    font = MOVE_LOG_FONT
    moveLogRect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANNEL_WIDTH, MOVE_LOG_PANNEL_HEIGHT)
    p.draw.rect(screen, p.Color('black'), moveLogRect)
    moveLog = []
    for i in range(0, len(gs.moveLog), 2):
        moveText = str(i // 2 + 1) + ".  " + gs.moveLog[i].getChessNotation()
        if i < len(gs.moveLog) - 1:
            moveText += "   " + gs.moveLog[i + 1].getChessNotation()
        moveLog.append(moveText)

    horizontalPadding = 5
    verticalPadding = 5
    lineSpacing = 5
    for i in range(len(moveLog)):
        textObject = font.render(moveLog[i], True, p.Color('white'))
        if (verticalPadding + textObject.get_height() >= (MOVE_LOG_PANNEL_HEIGHT - 1)):
            # if i > 1
            verticalPadding = 5
            horizontalPadding += 100
        textLocation = p.Rect(moveLogRect.move(horizontalPadding, verticalPadding))
        verticalPadding += textObject.get_height() + lineSpacing

        screen.blit(textObject, textLocation)
    if gs.checkMate:
        textObject = font.render("#", True, p.Color('Red'))
        textLocation = p.Rect(moveLogRect.move(horizontalPadding, verticalPadding))
        screen.blit(textObject, textLocation)
    if gs.staleMate:
        textObject = font.render("!", True, p.Color('Blue'))
        textLocation = p.Rect(moveLogRect.move(horizontalPadding, verticalPadding))
        screen.blit(textObject, textLocation)

def animateMove(move, screen, board, clock, whitesPerspective):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 3
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    drawEndRow, drawEndCol = move.endRow, move.endCol
    drawStartRow, drawStartCol = move.startRow, move.startCol
    if not whitesPerspective:
        drawStartRow, drawStartCol = blackPerspectiveRow(move.startRow, move.startCol)
        drawEndRow, drawEndCol = blackPerspectiveRow(move.endRow, move.endCol)
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        if not whitesPerspective:
            r, c = blackPerspectiveRow(r, c)
        drawBoard(screen)
        drawPieces(screen, board, whitesPerspective)
        color = colors[(drawEndRow + drawEndCol) % 2]
        endSqaure = p.Rect(drawEndCol * SQ_SIZE, drawEndRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSqaure)
        if move.pieceCaptured != '--':
            if move.enPassant:
                endSqaure = p.Rect(drawEndCol * SQ_SIZE, drawStartRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured], endSqaure)
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def drawEndGameText(screen, text):
    font = p.font.SysFont('Arial', 32, True, False)
    textObject = font.render(text, 0, p.Color('White'))
    textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - textObject.get_width() / 2, BOARD_HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2, 2))
    textObject = font.render(text, 0, p.Color('Blue'))
    screen.blit(textObject, textLocation.move(4, 4))

if __name__ == '__main__':
    main()