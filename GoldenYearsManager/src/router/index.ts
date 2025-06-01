import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { authApi } from '@/api/auth'
import type { RouteRecordRaw, RouteLocationNormalized } from 'vue-router'

declare module 'vue-router' {
  interface RouteMeta {
    public?: boolean
    requiresAuth?: boolean
    roles?: string[]
  }
}

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/auth/LoginView.vue'),
    meta: { public: true }
  },
  {
    path: '/person',
    name: 'person',
    component: () => import('@/views/person/PersonListView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/',
    redirect: '/person'
  },
  {
    path: '/person/create',
    name: 'person-create',
    component: () => import('@/views/person/PersonCreateView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/person/edit/:id',
    name: 'person-edit',
    component: () => import('@/views/person/PersonEditView.vue'),
    meta: { requiresAuth: true },
    props: true
  },
  {
    path: '/person/detail/:id',
    name: 'person-detail',
    component: () => import('@/views/person/PersonDetailView.vue'),
    meta: { requiresAuth: true },
    props: true
  },
  // 护理计划路由
  {
    path: '/care-plans',
    name: 'care-plan-list',
    component: () => import('@/views/care-plans/CarePlanListView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/care-plans/my',
    name: 'my-care-plan-list',
    component: () => import('@/views/care-plans/MyCarePlanListView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/care-plans/create',
    name: 'care-plan-create',
    component: () => import('@/views/care-plans/CarePlanCreateView.vue'),
    meta: { requiresAuth: true, roles: ['管理员', '护理主任'] }
  },
  {
    path: '/care-plans/:id',
    name: 'care-plan-detail',
    component: () => import('@/views/care-plans/CarePlanDetailView.vue'),
    meta: { requiresAuth: true },
    props: true
  },
  // 护理记录路由
  {
    path: '/care-records/create/:pid',
    name: 'care-record-create',
    component: () => import('@/views/care-records/CareRecordForm.vue'),
    meta: { requiresAuth: true, roles: ['护理工', '管理员'] }
  },
  {
    path: '/care-records/detail/:id',
    name: 'care-record-detail',
    component: () => import('@/views/care-records/CareRecordDetail.vue'),
    meta: { requiresAuth: true },
    props: true
  },
  {
    path: '/care-records/profile',
    name: 'profile-care-record-edit',
    component: () => import('@/views/care-records/ProfileCareRecordList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/care-records/person/:pid',
    name: 'pid-care-record-edit',
    component: () => import('@/views/care-records/PidCareRecordList.vue'),
    meta: { requiresAuth: true },
    props: true
  },
  // 用户管理路由
  {
    path: '/user',
    name: 'user-list',
    component: () => import('@/views/user/UserListView.vue'),
    meta: { requiresAuth: true, roles: ['管理员'] }
  },
  {
    path: '/user/create',
    name: 'user-create',
    component: () => import('@/views/user/UserCreateView.vue'),
    meta: { requiresAuth: true, roles: ['管理员'] }
  },
  {
    path: '/user/:id',
    name: 'user-detail',
    component: () => import('@/views/user/UserDetailView.vue'),
    meta: { requiresAuth: true, roles: ['管理员'] },
    props: true
  },
  {
    path: '/user/edit/:id',
    name: 'user-edit',
    component: () => import('@/views/user/UserEditView.vue'),
    meta: { requiresAuth: true, roles: ['管理员'] },
    props: true

  },

  // 个人主页路由
  {
    path: '/profile',
    name: 'profile',
    component: () => import('@/views/user/ProfileView.vue'),
    meta: { requiresAuth: true }
  },
  // 提醒路由
  {
    path: '/reminder/:pid',
    name: 'reminder-list',
    component: () => import('@/views/reminder/ReminderListView.vue'),
    meta: { requiresAuth: true },
    props: true
  },
  {
    path: '/reminder/:pid/create',
    name: 'reminder-create',
    component: () => import('@/views/reminder/ReminderForm.vue'),
    meta: { requiresAuth: true, roles: ['护理工', '管理员'] },
    props: true
  },
  {
    path: '/reminder/:pid/edit/:id',
    name: 'reminder-edit',
    component: () => import('@/views/reminder/ReminderForm.vue'),
    meta: { requiresAuth: true, roles: ['护理工', '管理员'] },
    props: true
  },

]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach(async (to: RouteLocationNormalized) => {
  const authStore = useAuthStore()

  // 检查token是否有效
  if (authStore.token) {
    try {
      const res = await authApi.verifyToken({ token: authStore.token })
      if (!res.isValid || res.isExpired) {
        throw new Error('Token无效或已过期')
      }
    } catch {
      await authStore.logout()
      return { name: 'login', query: { redirect: to.fullPath } }
    }
  }

  if (to.meta.requiresAuth && !authStore.token) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  if (to.meta.public && authStore.token) {
    return { name: 'person', query: { redirect: to.fullPath } }
  }

  // 检查角色权限
  if (to.meta.roles && !to.meta.roles.some(role => authStore.hasRole(role))) {
    return { name: 'person', query: { redirect: to.fullPath } }
  }
})

export default router
