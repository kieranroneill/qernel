// types
import type BaseErrorDetailResponse from './BaseErrorDetailResponse';

interface BaseErrorResponse<Detail extends BaseErrorDetailResponse> {
  detail: Detail;
}

export default BaseErrorResponse;
