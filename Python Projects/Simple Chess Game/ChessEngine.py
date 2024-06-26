import config

class GameState():
    def __init__(self):

        self.board = [['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
                      ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                      ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]

        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)

        self.inCheck = False
        self.pins = []
        self.checks = []
        self.checkMate = False
        self.staleMate = False

        self.enPassantPossible = ()
        self.enPassantLogs = [self.enPassantPossible]

        self.currentCastlingRights = CastleRights(True, True, True, True)
        self.castleRightsLog = [
            CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.wqs, self.currentCastlingRights.bks,
                         self.currentCastlingRights.bqs)]

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        if move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        if move.pawnPromotion:
            if (self.whiteToMove and config.PLAYER_ONE_HUMAN) or (not self.whiteToMove and config.PLAYER_TWO_HUMAN):
                promotedPiece = input("Enter your choice to Promote : Q, R, B or N : ")
            else:
                promotedPiece = 'Q'
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + promotedPiece

        if move.enPassant:
            self.board[move.startRow][move.endCol] = '--'

        if move.pieceMoved[1] == 'P' and abs(move.endRow - move.startRow) == 2:
            self.enPassantPossible = ((move.startRow + move.endRow) // 2, move.endCol)
        else:
            self.enPassantPossible = ()

        self.enPassantLogs.append(self.enPassantPossible)

        if move.isCastleMove:
            if move.endCol < move.startCol:
                self.board[move.endRow][0] = '--'
                self.board[move.endRow][move.endCol + 1] = move.pieceMoved[0] + 'R'
            else:
                self.board[move.endRow][7] = '--'
                self.board[move.endRow][move.endCol - 1] = move.pieceMoved[0] + 'R'

        self.updateCastlingRights(move)
        newCastleRights = CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.wqs,
                                       self.currentCastlingRights.bks, self.currentCastlingRights.bqs)
        self.castleRightsLog.append(newCastleRights)

        self.whiteToMove = not self.whiteToMove

    def undoMove(self):
        if len(self.moveLog) == 0:
            print('No move done till now. Can\'t UNDO at the start of the game')
            return
        move = self.moveLog.pop()
        self.board[move.startRow][move.startCol] = move.pieceMoved
        self.board[move.endRow][move.endCol] = move.pieceCaptured
        self.whiteToMove = not self.whiteToMove

        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.startRow, move.startCol)
        if move.pieceMoved == 'bK':
            self.blackKingLocation = (move.startRow, move.startCol)

        if move.enPassant:
            self.board[move.endRow][move.endCol] = '--'
            self.board[move.startRow][move.endCol] = move.pieceCaptured

        self.enPassantLogs.pop()
        self.enPassantPossible = self.enPassantLogs[-1]

        self.castleRightsLog.pop()
        self.currentCastlingRights.wks = self.castleRightsLog[-1].wks
        self.currentCastlingRights.wqs = self.castleRightsLog[-1].wqs
        self.currentCastlingRights.bks = self.castleRightsLog[-1].bks
        self.currentCastlingRights.bqs = self.castleRightsLog[-1].bqs

        if move.isCastleMove:
            if move.endCol < move.startCol:
                self.board[move.endRow][move.endCol + 1] = '--'
                self.board[move.endRow][0] = move.pieceMoved[0] + 'R'
            else:
                self.board[move.endRow][move.endCol - 1] = '--'
                self.board[move.endRow][7] = move.pieceMoved[0] + 'R'

        self.checkMate = False
        self.staleMate = False

    def updateCastlingRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRights.wqs = False
            self.currentCastlingRights.wks = False

        elif move.pieceMoved == 'bK':
            self.currentCastlingRights.bqs = False
            self.currentCastlingRights.bks = False

        elif move.pieceMoved == 'wR':
            if move.startRow == 7 and move.startCol == 0:
                self.currentCastlingRights.wqs = False
            if move.startRow == 7 and move.startCol == 7:
                self.currentCastlingRights.wks = False

        elif move.pieceMoved == 'bR':
            if move.startRow == 0 and move.startCol == 0:
                self.currentCastlingRights.bqs = False
            if move.startRow == 0 and move.startCol == 7:
                self.currentCastlingRights.bks = False

        if move.pieceCaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRights.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRights.wks = False
        if move.pieceCaptured == 'bR':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRights.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRights.bks = False

    def getValidMoves(self):
        tempCastlingRights = self.currentCastlingRights
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]

        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()

                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []
                if pieceChecking[1] == 'N':
                    validSquares.append((checkRow, checkCol))

                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[
                            1] == checkCol:
                            break
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K':
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])

            else:
                self.getKingMoves(kingRow, kingCol, moves)

        else:
            moves = self.getAllPossibleMoves()

        if len(moves) == 0:
            if self.inCheck:
                self.checkMate = True
        else:
            self.staleMate = False
            self.checkMate = False
        self.currentCastlingRights = tempCastlingRights

        self.getCastlingMoves(kingRow, kingCol, moves)
        return moves

    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            enemyColor = 'b'
            allyColor = 'w'
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = 'w'
            allyColor = 'b'
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for j in range(len(directions)):
            d = directions[j]
            possiblePins = ()
            for i in range(1, 8):
                endRow = startRow + (d[0] * i)
                endCol = startCol + (d[1] * i)
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[
                        1] != 'K':
                        if possiblePins == ():
                            possiblePins = (endRow, endCol, d[0], d[1])
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        pieceType = endPiece[1]

                        if (0 <= j <= 3 and pieceType == 'R') or \
                                (4 <= j <= 7 and pieceType == 'B') or \
                                (i == 1 and pieceType == 'P') and (
                                (enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5)) or \
                                (pieceType == 'Q') or \
                                (i == 1 and pieceType == 'K'):
                            if possiblePins == ():
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:
                                pins.append(possiblePins)
                                break
                        else:
                            break
                else:
                    break
        knightMoves = [(-1, -2), (-2, -1), (1, -2), (2, -1), (1, 2), (2, 1), (-1, 2), (-2, 1)]
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                piece = self.board[r][c][1]
                if not (self.whiteToMove ^ (turn == 'w')):
                    if piece != '-':
                        self.moveFunctions[piece](r, c, moves)
        return moves

    def getPawnMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove:
            moveAmount = -1
            startRow = 6
            backRow = 0
            enemyColor = 'b'
            kingRow, kingCol = self.whiteKingLocation
        else:
            moveAmount = 1
            startRow = 1
            backRow = 7
            enemyColor = 'w'
            kingRow, kingCol = self.blackKingLocation

        pawnPromotion = False

        if self.board[r + moveAmount][c] == '--':
            if not piecePinned or pinDirection == (moveAmount, 0):
                if r + moveAmount == backRow:
                    pawnPromotion = True
                moves.append(Move((r, c), (r + moveAmount, c), self.board, pawnPromotion=pawnPromotion))
                if r == startRow and self.board[r + (2 * moveAmount)][c] == '--':
                    moves.append(Move((r, c), (r + (2 * moveAmount), c), self.board))

        if c - 1 >= 0:
            if not piecePinned or pinDirection == (moveAmount, -1):
                if self.board[r + moveAmount][c - 1][0] == enemyColor:
                    if r + moveAmount == backRow:
                        pawnPromotion = True
                    moves.append(Move((r, c), (r + moveAmount, c - 1), self.board, pawnPromotion=pawnPromotion))
                if (r + moveAmount, c - 1) == self.enPassantPossible:
                    attackingPiece = blockingPiece = False
                    if kingRow == r:
                        if kingCol < c:
                            insideRange = range(kingCol + 1, c - 1)
                            outsideRange = range(c + 1, 8)
                        else:
                            insideRange = range(kingCol - 1, c, -1)
                            outsideRange = range(c - 2, -1, -1)
                        for i in insideRange:
                            if self.board[r][i] != '--':
                                blockingPiece = True
                                break
                        for i in outsideRange:
                            piece = self.board[r][i]
                            if piece[0] == enemyColor and (piece[1] == 'R' or piece[1] == 'Q'):
                                attackingPiece = True
                                break
                            elif piece != '--':
                                blockingPiece = True
                                break
                    if not attackingPiece or blockingPiece:
                        moves.append(Move((r, c), (r + moveAmount, c - 1), self.board, enPassant=True))

        if c + 1 < len(self.board):
            if not piecePinned or pinDirection == (moveAmount, 1):
                if self.board[r + moveAmount][c + 1][0] == enemyColor:
                    if r + moveAmount == backRow:
                        pawnPromotion = True
                    moves.append(Move((r, c), (r + moveAmount, c + 1), self.board, pawnPromotion=pawnPromotion))
                if (r + moveAmount, c + 1) == self.enPassantPossible:
                    attackingPiece = blockingPiece = False
                    if kingRow == r:
                        if kingCol < c:
                            insideRange = range(kingCol + 1, c)
                            outsideRange = range(c + 2, 8)
                        else:  # King to the right to the pawn
                            insideRange = range(kingCol - 1, c + 1, -1)
                            outsideRange = range(c - 1, -1, -1)
                        for i in insideRange:
                            if self.board[r][i] != '--':
                                blockingPiece = True
                                break
                        for i in outsideRange:
                            piece = self.board[r][i]
                            if piece[0] == enemyColor and (piece[1] == 'R' or piece[1] == 'Q'):
                                attackingPiece = True
                                break
                            elif piece != '--':
                                blockingPiece = True
                                break
                    if not attackingPiece or blockingPiece:
                        moves.append(Move((r, c), (r + moveAmount, c + 1), self.board, enPassant=True))

    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                endRow = r + (d[0] * i)
                endCol = c + (d[1] * i)
                if endRow >= 0 and endRow < len(self.board) and endCol >= 0 and endCol < len(self.board[endRow]):
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        if self.board[endRow][endCol] == '--':
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif self.board[endRow][endCol][0] == enemyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:
                            break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        piecePinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break

        if not piecePinned:
            directions = ((-1, -2), (-2, -1), (1, -2), (2, -1), (1, 2), (2, 1), (-1, 2), (-2, 1))
            allyColor = 'w' if self.whiteToMove else 'b'
            for d in directions:
                endRow = r + d[0]
                endCol = c + d[1]
                if endRow >= 0 and endRow < len(self.board) and endCol >= 0 and endCol < len(self.board[endRow]):
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                endRow = r + (d[0] * i)
                endCol = c + (d[1] * i)
                if endRow >= 0 and endRow < len(self.board) and endCol >= 0 and endCol < len(self.board[endRow]):
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        if self.board[endRow][endCol] == '--':  # Empty Square
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif self.board[endRow][endCol][0] == enemyColor:  # capture opponent's piece
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:
                            break
                else:
                    break

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = 'w' if self.whiteToMove else 'b'
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if endRow >= 0 and endRow < len(self.board) and endCol >= 0 and endCol < len(self.board[endRow]):
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:

                    if allyColor == 'w':
                        self.whiteKingLocation = (endRow, endCol)
                    if allyColor == 'b':
                        self.blackKingLocation = (endRow, endCol)

                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r, c), (endRow, endCol), self.board))

                    if allyColor == 'w':
                        self.whiteKingLocation = (r, c)
                    if allyColor == 'b':
                        self.blackKingLocation = (r, c)

    def getCastlingMoves(self, r, c, moves):
        if self.inCheck:
            return
        if (self.whiteToMove and self.currentCastlingRights.wks) or \
                (not self.whiteToMove and self.currentCastlingRights.bks):
            self.getKingSideCastleMoves(r, c, moves)

        if (self.whiteToMove and self.currentCastlingRights.wqs) or \
                (not self.whiteToMove and self.currentCastlingRights.bqs):
            self.getQueenSideCastleMoves(r, c, moves)

    def getKingSideCastleMoves(self, r, c, moves):
        if self.board[r][c + 1] == '--' and self.board[r][c + 2] == '--':
            if not self.isUnderAttack(r, c + 1) and not self.isUnderAttack(r, c + 2):
                moves.append(Move((r, c), (r, c + 2), self.board, isCastleMove=True))

    def getQueenSideCastleMoves(self, r, c, moves):
        if self.board[r][c - 1] == '--' and self.board[r][c - 2] == '--' and self.board[r][c - 3] == '--':
            if not self.isUnderAttack(r, c - 1) and not self.isUnderAttack(r, c - 2):
                moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove=True))

    def isUnderAttack(self, r, c):
        allyColor = 'w' if self.whiteToMove else 'b'
        enemyColor = 'b' if self.whiteToMove else 'w'
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        underAttack = False
        for j in range(len(directions)):
            d = directions[j]
            for i in range(1, 8):
                endRow = r + (d[0] * i)
                endCol = c + (d[1] * i)
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor:
                        break
                    elif endPiece[0] == enemyColor:
                        pieceType = endPiece[1]
                        if (0 <= j <= 3 and pieceType == 'R') or \
                                (4 <= j <= 7 and pieceType == 'B') or \
                                (i == 1 and pieceType == 'P') and (
                                (enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5)) or \
                                (pieceType == 'Q') or \
                                (i == 1 and pieceType == 'K'):

                            return True
                        else:
                            break
                else:
                    break
        if underAttack:
            return True
        knightMoves = [(-1, -2), (-2, -1), (1, -2), (2, -1), (1, 2), (2, 1), (-1, 2), (-2, 1)]
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    return True
        return False

class CastleRights:

    def __init__(self, wks, wqs, bks, bqs):
        self.wks = wks
        self.wqs = wqs
        self.bks = bks
        self.bqs = bqs

    def __str__(self):
        return ("7. Castling Rights(wk, wq, bk, bq) : " + str(self.wks) + " " + str(self.wqs) + " " + str(
            self.bks) + " " + str(self.bqs))

class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, enPassant=False, pawnPromotion=False, isCastleMove=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

        self.pawnPromotion = pawnPromotion
        self.isPawnPromotion = (self.pieceMoved == "wp" and self.endRow == 0) or (
                    self.pieceMoved == "bp" and self.endRow == 7)

        self.enPassant = enPassant
        if enPassant:
            self.pieceCaptured = 'bP' if self.pieceMoved == 'wP' else 'wP'

        self.isCastleMove = isCastleMove

        self.moveId = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def getChessNotation(self):
        return self.getFileRank(self.startRow, self.startCol) + self.getFileRank(self.endRow, self.endCol)

    def getFileRank(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    def __eq__(self, other):
        return isinstance(other, Move) and self.moveId == other.moveId
