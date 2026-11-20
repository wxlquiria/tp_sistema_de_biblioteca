class SocioError(Exception):
    pass


class SocioNoEncontradoError(SocioError):
    pass


class EmailDuplicadoError(SocioError):
    pass

class PrestamoError(Exception):
    
    pass


class SocioInactivoError(PrestamoError):
    pass


class MaxPrestamosActivosError(PrestamoError):
    pass


class LibroNoEncontradoError(PrestamoError):
    pass


class LibroSinStockError(PrestamoError):
    pass


class PrestamoNoEncontradoError(PrestamoError):
    pass


class PrestamoYaDevueltoError(PrestamoError):
    pass

class LibroError(Exception):
    pass


class LibroIsbnDuplicadoError(LibroError):
    pass


class AutorNoEncontradoError(LibroError):
    pass

class AutorError(Exception):
    pass
