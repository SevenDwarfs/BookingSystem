<template lang="jade">
  .register(v-loading="creating", element-loading-text="拼命创建用户中")
    el-steps.register__steps(space="30%", :active="currentStep", finish-status="success", :center="true", :align-center="true")
      el-step(title="步骤 1", description="输入用户名密码")
      el-step(title="步骤 2", description="绑定邮箱")
      el-step(title="步骤 3", description="绑定手机号")
    el-form.register__form(v-show="currentStep === 0", :model="userForm", :rules="userRules", ref="userForm", :inline="true", label-position="left")
      el-form-item(label="用户名", prop="username")
        el-input(v-model="userForm.username", @keyup.enter.native="passForm('userForm')")
      el-form-item(label="密码", prop="password")
        el-input(type="password", @keyup.enter.native="passForm('userForm')", v-model="userForm.password")
      el-form-item(label="重复密码", prop="repassword")
        el-input(type="password", @keyup.enter.native="passForm('userForm')", v-model="userForm.repassword")
      el-form-item
        el-button(type="primary", @click="passForm('userForm')") 确定
    el-form.register__form(v-show="currentStep === 1", :model="mailForm", :rules="emailRules", ref="mailForm", :inline="true", label-position="left")
      el-form-item(label="邮箱", prop="email")
        el-input(v-model="mailForm.email", @keyup.enter.native="passForm('mailForm')")
      el-form-item
        el-button(type="primary", @click="passForm('mailForm')") 确定
      el-form-item
        el-button(@click="back") 返回
    el-form.register__form(v-show="currentStep === 2", :model="phoneForm", :rules="phoneRules", ref="phoneForm", :inline="true", label-position="left")
      el-form-item(label="手机号", prop="phone")
        el-input(v-model="phoneForm.phone", @keyup.enter.native="passForm('phoneForm')")
      el-form-item
        el-button(type="primary", @click="passForm('phoneForm')") 确定
      el-form-item
        el-button(@click="back") 返回

</template>

<script>

import router from '@/router/index.js'
import { User } from '@/models/index.js'
const MAX_STEP = 3

export default {
  name: 'hello',
  data () {
    return {
      currentStep: 0,
      creating: false,
      userForm: {
        username: '',
        password: '',
        repassword: ''
      },
      userRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 6, max: 100, message: '用户名长度最低为6位', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, max: 100, message: '密码长度最低为6位', trigger: 'blur' }
        ],
        repassword: [
          { required: true, message: '请确认密码', trigger: 'blur' },
          { validator: this.confirmPassValid, trigger: 'blur' }
        ]
      },
      mailForm: {
        email: ''
      },
      emailRules: {
        email: [
          { required: true, message: '请输入邮箱', trigger: 'blur' },
          { validator: this.emailValid, trigger: 'blur' }
        ]
      },
      phoneForm: {
        phone: ''
      },
      phoneRules: {
        phone: [
          { required: true, message: '请输入手机号码', trigger: 'blur' },
          { validator: this.phoneValid, trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    confirmPassValid (rule, value, callback) {
      if (value !== this.userForm.password) {
        callback(new Error('输入密码不一致!'))
      } else {
        callback()
      }
    },
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
    pass () {
      this.currentStep = this.currentStep + 1 <= MAX_STEP ? this.currentStep + 1 : MAX_STEP
      if (this.currentStep === MAX_STEP) {
        this.creating = true
        let submitForm = {
          username: this.userForm.username,
          password: this.userForm.password,
          email: this.mailForm.email,
          phone: this.phoneForm.phone
        }
        User.signup(submitForm).then(res => {
          this.creating = false
          if (res.stateCode === '200') {
            this.$message.success('创建成功，请登录')
            router.push({ name: 'Home' })
          } else {
            this.$message.error(res.info)
          }
        }).catch(() => {
          this.creating = false
          this.$message.error('创建失败')
          this.back()
        })
      }
    },
    back () {
      this.currentStep = this.currentStep - 1 >= 0 ? this.currentStep - 1 : 0
    },
    passForm (formname) {
      this.$refs[formname].validate((valid) => {
        if (valid) {
          this.pass()
        } else {
          this.$message.error('表单错误')
        }
      })
    },
    passUser () {
      this.$refs['userForm'].validate((valid) => {
        if (valid) {
          this.pass()
        } else {
          this.$message.error('表单错误')
        }
      })
    },
    passEmail () {
      this.$refs['mailForm'].validate((valid) => {
        if (valid) {
          this.pass()
        } else {
          this.$message.error('表单错误')
        }
      })
    },
    passPhone () {
      this.$refs['phoneForm'].validate((valid) => {
        if (valid) {
          this.pass()
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

  .register .register__steps {
    padding-top: 40px;
  }

  .register .register__form {
    padding-top: 80px;
  }

</style>
