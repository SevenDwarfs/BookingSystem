<template lang="jade">
  .profile
    el-form.user(:model="user", :rules="rules", ref="user")
      img.user__avatar(:src="user.avatar")
      .user__info-container
        el-form-item.user__info(prop="username")
          .user__info__title 用户名：
          el-input.user__info__text(v-model="user.username", :disabled="true")
        el-form-item.user__info(prop="email")
          .user__info__title 邮箱：
          el-input.user__info__text(v-model="user.email")
        el-form-item.user__info(prop="phone")
          .user__info__title 电话：
          el-input.user__info__text(v-model="user.phone")
        .operation.operation--save(@click="update") 保存
      //- .operation.operation--avatar 更改头像


</template>

<script>

import { User } from '@/models/index.js'

export default {
  name: 'hello',
  data () {
    return {
      user: {
        username: '',
        email: '',
        phone: '',
        avatar: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 6, max: 100, message: '用户名长度最低为6位', trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入邮箱', trigger: 'blur' },
          { validator: this.emailValid, trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入手机号码', trigger: 'blur' },
          { validator: this.phoneValid, trigger: 'blur' }
        ]
      }
    }
  },
  created () {
    User.fetchInfo().then(res => {
      this.user = res
      this.user.username = res.userName
      this.user.avatar = 'http://p0.meituan.net/movie/7dd82a16316ab32c8359debdb04396ef2897.png'
    })
  },
  methods: {
    emailValid (rule, value, callback) {
      const emailPattern = /[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?/
      if (!emailPattern.test(value)) {
        callback(new Error('邮箱格式不正确'))
      } else {
        callback()
      }
    },
    phoneValid (rule, value, callback) {
      const phonePattern = /^1[34578]\d{9}$/
      if (!phonePattern.test(value)) {
        callback(new Error('手机号码格式不正确'))
      } else {
        callback()
      }
    },
    update () {
      this.$refs['user'].validate((valid) => {
        if (valid) {
          User.updateInfo(this.user).then(res => {
            if (res.stateCode === '200') {
              this.$message.success('修改成功')
            } else {
              this.$message.error(res.info)
            }
          }).catch(() => {
            this.$message.error('修改失败')
          })
        } else {
          this.$message.error('表单错误')
        }
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

  .user {
    padding-top: 100px;
    margin: 0px 130px;
    position: relative;
    overflow: visible;
  }

  .user__avatar {
    position: absolute;
    left: 50px;
    border-radius: 50%;
    top: 30px;
    height: 140px;
    border: 1px solid #efefef;
    width: 140px;
    padding: 6px;
    box-sizing: border-box;
    background: #fff;
  }

  .user__info-container {
    border: 1px solid #efefef;
    padding: 60px;
    padding-left: 250px;
    text-align: left;
    border-radius: 10px;
    box-shadow: 0px 0px 2px #eee;
    padding-bottom: 100px;
  }

  .user__info__title, .user__info__text {
    display: inline-block;
    text-align: left;
    font-size: 18px;
  }

  .user__info__title {
    width: 100px;
    font-weight: bold;
    margin-right: 0px;
  }

  .user__info__text {
  }

  .operation {
    width: 100px;
    padding: 8px 20px;
    background: #20A0FF;
    color: #fff;
    font-weight: 700;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    text-align: center;
  }

  .operation--avatar {
    position: absolute;
    left: 50px;
    top: 250px;
  }

  .operation--save {
    position: absolute;
    bottom: 40px;
    right: 60px;
  }

</style>
