<template>
  <div>
    <div class="text-center mb-8">
      <h1 class="brand-title">Lucky Cat Coffee & Kitchen</h1>
      <p class="brand-subtitle">STAFF PORTAL REGISTRATION</p>
    </div>

    <form @submit.prevent="handleRegister" class="space-y-5">
      <div class="form-group">
        <label class="input-label">
          <UserIcon :size="18" />
          Full Name
        </label>
        <input type="text" v-model="form.full_name" class="input auth-input" placeholder="Julian Thorne" required />
      </div>

      <div class="form-group">
        <label class="input-label">
          <MailIcon :size="18" />
          Email Address
        </label>
        <input type="email" v-model="form.email" class="input auth-input" placeholder="j.thorne@luckycat.com" required />
      </div>

      <div class="form-group">
        <label class="input-label">
          <BriefcaseIcon :size="18" />
          Role Selection
        </label>
        <div class="role-grid">
          <button
            v-for="role in roles"
            :key="role.value"
            type="button"
            :class="['role-btn', { active: form.role === role.value }]"
            @click="form.role = role.value"
          >
            {{ role.label }}
          </button>
        </div>
      </div>

      <div class="form-group">
        <label class="input-label">
          <LockIcon :size="18" />
          Password
        </label>
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
      <p v-if="success" style="text-align:center; font-size:0.875rem; color:var(--success);">{{ success }}</p>

      <button type="submit" class="btn-auth" :disabled="loading || !form.role">
        <template v-if="loading">
          <span class="spinner-sm" />
          Creating Account...
        </template>
        <template v-else>Create Account</template>
      </button>
    </form>

    <div class="auth-footer">
      <p>Already have an account? <router-link to="/login" class="auth-link">Login</router-link></p>
    </div>

    <div class="bottom-links">
      <a href="#">Privacy Policy</a>
      <a href="#">Terms of Service</a>
      <a href="#">Contact Us</a>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '../../api/auth'
import { UserIcon, MailIcon, BriefcaseIcon, LockIcon, EyeIcon, EyeOffIcon } from 'lucide-vue-next'

const router = useRouter()
const form = reactive({ full_name: '', email: '', password: '', role: 'cashier' })
const error = ref('')
const success = ref('')
const loading = ref(false)
const showPassword = ref(false)

const roles = [
  { label: 'Cashier', value: 'cashier' },
  { label: 'Barista', value: 'cashier' },
  { label: 'Manager', value: 'admin' },
]

async function handleRegister() {
  error.value = ''
  success.value = ''
  loading.value = true
  try {
    await register(form)
    success.value = 'Registration successful! Please login.'
    setTimeout(() => router.push('/login'), 1500)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Registration failed. Try again.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.brand-title {
  font-family: Georgia, 'Times New Roman', serif;
  font-size: 1.75rem;
  font-weight: 700;
  color: #2D2D2D;
  margin-bottom: 0.125rem;
}
.brand-subtitle {
  font-size: 0.75rem;
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
.input-wrapper { position: relative; }
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
.role-grid {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}
.role-btn {
  flex: 1;
  min-width: 100px;
  padding: 0.625rem 1rem;
  border-radius: 999px;
  font-weight: 500;
  font-size: 0.8125rem;
  border: 2px solid #2D2D2D;
  background: #fff;
  color: #2D2D2D;
  cursor: pointer;
  transition: all 0.2s;
}
.role-btn:hover { border-color: #3D2817; }
.role-btn.active {
  background: #3D2817;
  color: #fff;
  border-color: #3D2817;
}
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
  margin-top: 1rem;
}
.btn-auth:hover:not(:disabled) { transform: scale(1.03); }
.btn-auth:active:not(:disabled) { transform: scale(0.97); }
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
