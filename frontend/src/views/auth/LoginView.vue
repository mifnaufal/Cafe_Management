<template>
  <div>
    <div class="text-center mb-8">
      <h1 class="brand-title">Lucky Cat</h1>
      <p class="brand-subtitle">COFFEE & KITCHEN</p>
    </div>

    <form @submit.prevent="handleLogin" class="space-y-5">
      <div class="form-group">
        <label class="input-label">
          <MailIcon :size="18" />
          Staff Email
        </label>
        <div class="input-wrapper">
          <input
            v-model="form.email"
            type="email"
            class="input auth-input"
            placeholder="name@luckycat.coffee"
            required
          />
          <MailIcon :size="20" class="input-icon" />
        </div>
      </div>

      <div class="form-group">
        <div class="flex items-center justify-between">
          <label class="input-label">
            <LockIcon :size="18" />
            Password
          </label>
          <a href="#" class="forgot-link">Forgot Password?</a>
        </div>
        <div class="input-wrapper">
          <input
            :type="showPassword ? 'text' : 'password'"
            v-model="form.password"
            class="input auth-input"
            placeholder="••••••••"
            required
          />
          <button type="button" class="toggle-password" @click="showPassword = !showPassword">
            <EyeOffIcon v-if="showPassword" :size="20" />
            <EyeIcon v-else :size="20" />
          </button>
        </div>
      </div>

      <p v-if="error" class="form-error" style="text-align:center;">{{ error }}</p>

      <button type="submit" class="btn-auth" :disabled="loading">
        <template v-if="loading">
          <span class="spinner-sm" />
          Logging in...
        </template>
        <template v-else>
          Login to Terminal <span style="margin-left:0.25rem;">&rarr;</span>
        </template>
      </button>
    </form>

    <div class="auth-footer">
      <p>New staff member? <router-link to="/register" class="auth-link">Sign Up</router-link></p>
    </div>

    <div class="bottom-links">
      <a href="#">Privacy Policy</a>
      <a href="#">Staff Support</a>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { MailIcon, LockIcon, EyeIcon, EyeOffIcon } from 'lucide-vue-next'

const router = useRouter()
const auth = useAuthStore()

const form = reactive({ email: '', password: '' })
const error = ref('')
const loading = ref(false)
const showPassword = ref(false)

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    await auth.login(form.email, form.password)
    router.push('/dashboard')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Login failed. Check email and password.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.brand-title {
  font-family: Georgia, 'Times New Roman', serif;
  font-size: 2.5rem;
  font-weight: 700;
  color: #2D2D2D;
  margin-bottom: 0.25rem;
}
.brand-subtitle {
  font-size: 0.8125rem;
  letter-spacing: 0.15em;
  color: #6B6B6B;
  font-weight: 500;
}
.space-y-5 > * + * { margin-top: 1.25rem; }
.input-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #2D2D2D;
  margin-bottom: 0.5rem;
}
.input-wrapper {
  position: relative;
}
.auth-input {
  width: 100%;
  padding: 0.75rem 1rem;
  background: #E8F5E8;
  border: 2px solid #E8F5E8;
  border-radius: 12px;
  font-size: 0.875rem;
  color: #2D2D2D;
  outline: none;
  transition: border-color 0.2s;
}
.auth-input::placeholder { color: #9CA697; }
.auth-input:focus { border-color: #3D2817; }
.input-icon {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #9CA697;
  pointer-events: none;
}
.toggle-password {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #9CA697;
  cursor: pointer;
  padding: 0.25rem;
}
.forgot-link {
  font-size: 0.8125rem;
  color: #FF6B4A;
  font-weight: 500;
  text-decoration: none;
}
.forgot-link:hover { color: #e55a3d; }
.btn-auth {
  width: 100%;
  background: #3D2817;
  color: #fff;
  font-weight: 600;
  padding: 0.875rem;
  border: none;
  border-radius: 999px;
  font-size: 0.9375rem;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 1.5rem;
}
.btn-auth:hover:not(:disabled) {
  transform: scale(1.03);
}
.btn-auth:active:not(:disabled) {
  transform: scale(0.97);
}
.btn-auth:disabled { opacity: 0.5; cursor: not-allowed; }
.spinner-sm {
  width: 1rem; height: 1rem;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.auth-footer {
  text-align: center;
  margin-top: 1.5rem;
  font-size: 0.875rem;
  color: #2D2D2D;
}
.auth-link {
  color: #FF6B4A;
  font-weight: 600;
  text-decoration: none;
}
.auth-link:hover { text-decoration: underline; }
.bottom-links {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin-top: 2rem;
  font-size: 0.75rem;
  color: #6B6B6B;
}
.bottom-links a { color: inherit; text-decoration: none; }
.bottom-links a:hover { color: #2D2D2D; }
</style>
