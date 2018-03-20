import position


class Validate:
    def __init__(self):
        self.short_castle_white = True
        self.short_castle_black = True
        self.long_castle_white = True
        self.long_castle_black = True
        self.en_passant_white = [False, 'capture position', 'delete pawn position']
        self.en_passant_black = [False, 'capture position', 'delete pawn position']

    def validatePawn(self, active_piece, at_position, to_position, unit_direction, gameboard):
        step = to_position.subtract(at_position)
        one_step, two_step, capture = self.convertStrPositionToObjPosition('a2', 'a3', 'b2')
        capture_left = capture.subtract(position.Position('c1'))
        capture_right = capture.subtract(position.Position('a1'))
        passive_piece = gameboard.getPieceAtPosition(str(to_position))
        if active_piece.hasColor('black'):
            one_step = one_step.invert()
            two_step = two_step.invert()
            capture_left = capture_right.invert()
            capture_right = capture_left.invert()
        if (step == capture_left or step == capture_right) and passive_piece is not None:
            return True
        elif step == one_step and passive_piece is None:
            return self.checkSquaresForBlockingPiecesRecursive(at_position, to_position.add(unit_direction), unit_direction, gameboard)
        elif active_piece.start_position and step == two_step and passive_piece is None:
            if self.checkSquaresForBlockingPiecesRecursive(at_position, to_position.add(unit_direction), unit_direction, gameboard):
                capture_position = at_position.add(one_step)
                delete_pawn_position = at_position.add(two_step)
                if active_piece.hasColor('white'):
                    self.en_passant_black = [True, str(capture_position), str(delete_pawn_position)]
                else:
                    self.en_passant_white = [True, str(capture_position), str(delete_pawn_position)]
                return True
        else:
            return False


    def validateRook(self, active_piece, at_position, to_position, unit_direction, gameboard):
        if unit_direction.columnLength() == 0 or unit_direction.rowLength() == 0:
            if self.checkSquaresForBlockingPiecesRecursive(at_position, to_position.add(unit_direction), unit_direction, gameboard):
                if active_piece.isAtPosition('a1') or active_piece.isAtPosition('a8'):
                    self.setLongCastleFlagToFalse(active_piece.color)
                else:
                    self.setShortCastleFlagToFalse(active_piece.color)
                return True
            else:
                return False
        else:
            return False

    def validateKnight(self, active_piece, at_position, to_position, unit_direction, gameboard):
        difference = to_position.subtract(at_position)
        length = difference.length()
        if length == 3 and (difference.columnLength() == 1 or difference.columnLength() == 2):
            return True
        else:
            return False

    def validateBishop(self, active_piece, at_position, to_position, unit_direction, gameboard):
        difference = at_position.subtract(to_position)
        if difference.columnLength() == difference.rowLength():
            return self.checkSquaresForBlockingPiecesRecursive(at_position, to_position.add(unit_direction), unit_direction, gameboard)
        else:
            return False

    def validateQueen(self, active_piece, at_position, to_position, unit_direction, gameboard):
        difference = at_position.subtract(to_position)
        if difference.columnLength() == 0 or difference.rowLength() == 0 or (difference.columnLength() == difference.rowLength()):
            return self.checkSquaresForBlockingPiecesRecursive(at_position, to_position.add(unit_direction), unit_direction, gameboard)
        else:
            return False

    def validateKing(self, active_piece, at_position, to_position, unit_direction, gameboard):
        difference = at_position.subtract(to_position)
        if difference.length() == 1:
            if self.checkSquaresForBlockingPiecesRecursive(at_position, to_position.add(unit_direction), unit_direction, gameboard):
                self.setShortCastleFlagToFalse(active_piece.color)
                self.setLongCastleFlagToFalse(active_piece.color)
                return True
            else:
                return False
        else:
            return False

    def validateShortCastle(self, color, gameboard):
        short_castle = self.short_castle_white if color == 'white' else self.short_castle_black
        self.setShortCastleFlagToFalse(color)
        return short_castle

    def validateLongCastle(self, color, gameboard):
        long_castle = self.long_castle_white if color == 'white' else self.long_castle_black
        self.setLongCastleFlagToFalse(color)
        return long_castle

    def setShortCastleFlagToFalse(self, color):
        if color == 'white':
            self.short_castle_white = False
        else:
            self.short_castle_black = False

    def setLongCastleFlagToFalse(self, color):
        if color == 'white':
            self.long_castle_white = False
        else:
            self.long_castle_black = False

    def validateEnPassant(self, active_piece, color, gameboard):
        en_passant = self.en_passant_white if color == 'white' else self.en_passant_black
        return en_passant[0]

    def isKingInCheck(self, active_piece, gameboard):
        king = gameboard.getWhiteKing() if active_piece.hasColor('white') else gameboard.getBlackKing()
        pieces = gameboard.getAllBlackPieces() if active_piece.hasColor('white') else gameboard.getAllWhitePieces()
        for piece in pieces:
            tmp = self.validatePieceMove(piece, piece.getPosition(), king.getPosition(), gameboard)
            if tmp:
                return True
        return False

    def validatePieceMove(self, active_piece, at_position, to_position, gameboard):
        validate_functions = {'pawn': self.validatePawn, 'rook': self.validateRook, 'knight': self.validateKnight,
                              'bishop': self.validateBishop, 'queen': self.validateQueen, 'king': self.validateKing}
        at_position, to_position = self.convertStrPositionToObjPosition(at_position, to_position)
        unit_direction = at_position.subtract(to_position).unit()
        validate_function = validate_functions[active_piece.getPieceName()]
        valid_move = validate_function(active_piece, at_position, to_position, unit_direction, gameboard)
        return valid_move

    def validateMove(self, active_piece, at_position, to_position, gameboard):
        if self.validatePieceMove(active_piece, at_position, to_position, gameboard):
            passive_piece = self.temporarelyMoveActivePiece(active_piece, at_position, to_position, gameboard)
            king_is_in_check = self.isKingInCheck(active_piece, gameboard)
            self.moveActivePiceBack(active_piece, passive_piece, at_position, to_position, gameboard)
            if not king_is_in_check:
                return True
            else:
                return False
        else:
            return False

    def moveActivePiceBack(self, active_piece, passive_piece, at_position, to_position, gameboard):
        if passive_piece is None:
            del gameboard.board_state[to_position]
        else:
            gameboard.board_state[to_position] = passive_piece
        gameboard.board_state[at_position] = active_piece

    def temporarelyMoveActivePiece(self, active_piece, at_position, to_position, gameboard):
        passive_piece = gameboard.getPieceAtPosition(to_position)
        del gameboard.board_state[at_position]
        gameboard.board_state[to_position] = active_piece
        return passive_piece

    def convertStrPositionToObjPosition(self, *arg):
        positions = []
        for board_position in arg:
            positions.append(position.Position(board_position))
        return positions

    def checkSquaresForBlockingPiecesRecursive(self, at_position, check_position, unit_direction, gameboard):
        if check_position == at_position:
            return True
        passive_piece = gameboard.getPieceAtPosition(str(check_position))
        if passive_piece is not None:
            return False
        return self.checkSquaresForBlockingPiecesRecursive(at_position, check_position.add(unit_direction), unit_direction, gameboard)

