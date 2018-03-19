import position




def validatePawn(active_piece, at_position, to_position, unit_direction, gameboard):
    step = to_position.subtract(at_position)
    one_step, two_step, capture = convertStrPositionToObjPosition('a2', 'a3', 'b2')
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
        return checkSquaresForBlockingPiecesRecursive(at_position, to_position.add(unit_direction), unit_direction, gameboard)
    elif active_piece.start_position and step == two_step and passive_piece is None:
        return checkSquaresForBlockingPiecesRecursive(at_position, to_position.add(unit_direction), unit_direction, gameboard)
    else:
        return False


def validateRook(active_piece, at_position, to_position, unit_direction, gameboard):
    if unit_direction.isColumnOrRowCoordinateZero():
        return checkSquaresForBlockingPiecesRecursive(at_position, to_position.add(unit_direction), unit_direction, gameboard)
    else:
        return False

def validateKnight(active_piece, at_position, to_position, unit_direction, gameboard):
    return True

def validateBishop(active_piece, at_position, to_position, unit_direction, gameboard):
    return True

def validateQueen(active_piece, at_position, to_position, unit_direction, gameboard):
    return True

def validateKing(active_piece, at_position, to_position, unit_direction, gameboard):
    return True

def isKingInCheck(active_piece, gameboard):
    king = gameboard.getWhiteKing() if active_piece.hasColor('white') else gameboard.getBlackKing()
    pieces = gameboard.getAllBlackPieces() if active_piece.hasColor('white') else gameboard.getAllWhitePieces()
    for piece in pieces:
        if piece.hasName('knight'):
            continue
        if piece.hasName('bishop'):
            continue
        if piece.hasName('queen'):
            continue
        if piece.hasName('king'):
            continue
        is_king_in_check = validatePieceMove(piece, str(piece.getPosition()), str(king.getPosition()), gameboard)
        if is_king_in_check:
            return True
    return False

def validatePieceMove(active_piece, at_position, to_position, gameboard):
    validate_functions = {'pawn': validatePawn, 'rook': validateRook, 'knight': validateKnight,
                          'bishop': validateBishop, 'queen': validateQueen, 'king': validateKing}
    at_position, to_position = convertStrPositionToObjPosition(at_position, to_position)
    unit_direction = at_position.subtract(to_position).unit()
    validate_function = validate_functions[active_piece.getPieceName()]
    valid_move = validate_function(active_piece, at_position, to_position, unit_direction, gameboard)
    return valid_move

def validateMove(active_piece, at_position, to_position, gameboard):
    valid_move = validatePieceMove(active_piece, at_position, to_position, gameboard)
    is_king_in_check = isKingInCheck(active_piece, gameboard)
    if not is_king_in_check and valid_move:
        return True
    else:
        return False

def convertStrPositionToObjPosition(*arg):
    positions = []
    for board_position in arg:
        positions.append(position.Position(board_position))
    return positions


def checkSquaresForBlockingPiecesRecursive(at_position, check_position, unit_direction, gameboard):
    if check_position == at_position:
        return True
    passive_piece = gameboard.getPieceAtPosition(str(check_position))
    if passive_piece is not None:
        return False
    return checkSquaresForBlockingPiecesRecursive(at_position, check_position.add(unit_direction), unit_direction, gameboard)

