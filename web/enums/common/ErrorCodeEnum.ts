enum ErrorCodeEnum {
  // general
  UnknownError = 1000,

  // builds
  TemplateNotFoundError = 2000,

  // authentication
  UnauthorizedError = 4001,
  ForbiddenError = 4003,

  // network
  InternalServerError = 5000,
  ParsingError = 5001,
}

export default ErrorCodeEnum;
