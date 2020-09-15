import request from '@/utils/request'

export function get##model_camel_case_name##s() {
  return request({
    url: 'api/##model_name##s/',
    method: 'get'
  })
}

export function add(data) {
  return request({
    url: 'api/##model_name##s/',
    method: 'post',
    data
  })
}

export function del(id) {
  return request({
    url: 'api/##model_name##s/' + id + '/',
    method: 'delete'
  })
}

export function edit(id, data) {
  return request({
    url: 'api/##model_name##s/' + id + '/',
    method: 'put',
    data
  })
}
