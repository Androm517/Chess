import position


class Validate:
    def __init__(self):
        self.white_castle = True
        self.black_castle = True
        self.en_passant = []

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
            return self.checkSquaresForBlockingPiecesRecursive(at_position, to_position.add(unit_direction), unit_direction, gameboard)
        else:
            return False


    def validateRook(self, active_piece, at_position, to_position, unit_direction, gameboard):
        if unit_direction.columnLength() == 0 or unit_direction.rowLength() == 0:
            return self.checkSquaresForBlockingPiecesRecursive(at_position, to_position.add(unit_direction), unit_direction, gameboard)
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
            return self.checkSquaresForBlockingPiecesRecursive(at_position, to_position.add(unit_direction), unit_direction, gameboard)
        else:
            return False

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
            passive_piece = self.temporarelyMoveActivePiece(active_piece, at_position, gameboard, to_position)
            king_is_in_check = self.isKingInCheck(active_piece, gameboard)
            self.moveActivePiceBack(active_piece, at_position, gameboard, passive_piece, to_position)
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

