<template>
  <div class="user-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>用户列表</span>
          <el-button type="primary" @click="handleAdd" v-if="authStore.user?.role === '管理员'">
            新增用户
          </el-button>
        </div>
      </template>

      <el-form :model="query" inline>
        <el-form-item label="用户名">
          <el-input v-model="query.username" placeholder="请输入用户名" clearable />
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="query.realName" placeholder="请输入姓名" clearable />
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="query.role" placeholder="请选择" clearable style="width: 200px">
            <el-option label="管理员" value="管理员" />
            <el-option label="护理主任" value="护理主任" />
            <el-option label="护理工" value="护理工" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">搜索</el-button>
          <el-button @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="list" border style="width: 100%">
        <el-table-column prop="username" label="用户名" width="150" />
        <el-table-column prop="realName" label="姓名" width="120" />
        <el-table-column prop="role" label="角色" width="120">
          <template #default="scope">
            <el-tag :type="getRoleTagType(scope.row.role)">
              {{ scope.row.role }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="phone" label="电话" width="150" />
        <el-table-column label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.isActivate ? 'success' : 'danger'">
              {{ scope.row.isActivate ? '激活' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180">
          <template #default="scope">
            <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button
              size="small"
              type="danger"
              @click="handleDelete(scope.row)"
              v-if="authStore.user?.role === '管理员'"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        class="pagination"
        v-model:current-page="query.page"
        v-model:page-size="query.pageSize"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="fetchData"
        @current-change="fetchData"
      />
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getUserList, deleteUser } from '@/api/user'
import { useAuthStore } from '@/stores/auth'
import type { User } from '@/types'

const list = ref<User[]>([])
const total = ref(0)
const query = ref({
  page: 1,
  pageSize: 10,
  username: '',
  realName: '',
  role: '',
})

const router = useRouter()
const authStore = useAuthStore()

const fetchData = async () => {
  try {
    const res = await getUserList({
      skip: (query.value.page - 1) * query.value.pageSize,
      limit: query.value.pageSize,
      username: query.value.username,
      name: query.value.realName,
      role: query.value.role,
    })
    list.value = res.data
    total.value = res.data.length
  } catch (error) {
    console.error('获取用户列表失败:', error)
    ElMessage.error('获取用户列表失败')
  }
}

const resetQuery = () => {
  query.value = {
    page: 1,
    pageSize: 10,
    username: '',
    realName: '',
    role: '',
  }
  fetchData()
}

const getRoleTagType = (role: string) => {
  switch (role) {
    case '管理员':
      return 'danger'
    case '护理主任':
      return 'warning'
    default:
      return 'success'
  }
}

const handleAdd = () => {
  router.push('/user/create')
}

const handleEdit = (row: User) => {
  router.push(`/user/edit/${row.uid}`)
}

const handleDelete = async (row: User) => {
  try {
    await ElMessageBox.confirm('确定要删除该用户吗?', '提示', {
      type: 'warning',
    })
    await deleteUser(row.uid)
    ElMessage.success('删除成功')
    await fetchData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除用户失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

// 初始化加载数据
fetchData()
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.pagination {
  margin-top: 20px;
  justify-content: flex-end;
}
</style>
