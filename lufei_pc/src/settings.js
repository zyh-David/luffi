export default {
  Host:"http://api.luffycity.cn:8000",
  check_user_login() {
    let token = localStorage.user_token || sessionStorage.user_token
    return token
  },
}
