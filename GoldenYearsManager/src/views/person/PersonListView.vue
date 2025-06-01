<template>
  <div class="person-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>人员列表</span>
          <el-button type="primary" @click="handleAdd">新增人员</el-button>
        </div>
      </template>

      <el-form :model="query" inline>
        <el-form-item label="姓名">
          <el-input v-model="query.name" placeholder="请输入姓名" clearable />
        </el-form-item>
        <el-form-item label="人员类型">
          <el-select v-model="query.category" placeholder="请选择" clearable style="width: 200px">
            <el-option label="孤寡老人" value="孤寡老人" />
            <el-option label="残障人士" value="残障人士" />
            <el-option label="短期托管" value="短期托管" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="query.status" placeholder="请选择" clearable style="width: 200px">
            <el-option label="在院" value="in" />
            <el-option label="出院" value="out" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">搜索</el-button>
          <el-button @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="list" border style="width: 100%">
        <el-table-column label="照片" width="100">
          <template #default="scope">
            <el-image
              v-if="scope.row.photo"
              :src="scope.row.photo"
              :preview-src-list="[scope.row.photo]"
              fit="cover"
              style="width: 60px; height: 60px"
            />
            <el-avatar v-else :size="60" icon="el-icon-user-solid" />
          </template>
        </el-table-column>
        <el-table-column prop="name" label="姓名" width="120" />
        <el-table-column prop="gender" label="性别" width="80" />
        <el-table-column prop="age" label="年龄" width="80" />
        <el-table-column prop="bedNumber" label="床位号" />
        <el-table-column prop="category" label="人员类型" />
        <el-table-column prop="checkInDate" label="入院日期" width="120" />
        <el-table-column label="状态" width="80">
          <template #default="scope">
            <el-tag :type="scope.row.checkOutDate ? 'info' : 'success'">
              {{ scope.row.checkOutDate ? '出院' : '在院' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="240">
          <template #default="scope">
            <el-button
              size="small"
              @click="handleEdit(scope.row)"
              v-if="authStore.hasRole('管理员') || authStore.hasRole('护理主任')"
              >编辑</el-button
            >
            <el-button
              size="small"
              type="danger"
              @click="handleDelete(scope.row)"
              v-if="authStore.hasRole('管理员') || authStore.hasRole('护理主任')"
              >删除</el-button
            >
            <el-button
              size="small"
              type="warning"
              @click="handleRecord(scope.row)"
              v-if="authStore.hasRole('护理工')"
              >护理记录</el-button
            >
            <el-button size="small" type="primary" @click="handleDetail(scope.row)">详情</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        class="pagination"
        v-model:current-page="query.page"
        v-model:page-size="query.page_size"
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
import { useAuthStore } from '@/stores/auth'
import { personApi } from '@/api/person'
import type { PersonListItem } from '@/api/person'
import { ElMessageBox, ElMessage } from 'element-plus'

const authStore = useAuthStore()

const list = ref<PersonListItem[]>([])
const total = ref(0)
const query = ref({
  page: 1,
  page_size: 10,
  name: '',
  category: '',
  status: '',
})

const router = useRouter()

const fetchData = async () => {
  try {
    const res = await personApi.getList({
      page: query.value.page,
      page_size: query.value.page_size,
      name: query.value.name,
      category: query.value.category,
      status: query.value.status,
    })
    list.value = res.items
    total.value = res.total
  } catch (error) {
    console.error('获取人员列表失败:', error)
  }
}

const resetQuery = () => {
  query.value = {
    page: 1,
    page_size: 10,
    name: '',
    category: '',
    status: '',
  }
  fetchData()
}

const handleAdd = () => {
  router.push('/person/create')
}

const handleEdit = (row: PersonListItem) => {
  router.push(`/person/edit/${row.pid}`)
}

const handleDetail = (row: PersonListItem) => {
  router.push(`/person/detail/${row.pid}`)
}

const handleRecord = (row: PersonListItem) => {
  router.push(`/care-records/person/${row.pid}`)
}

const handleDelete = async (row: PersonListItem) => {
  try {
    await ElMessageBox.confirm('确定要删除该人员吗?', '提示', {
      type: 'warning',
    })
    await personApi.delete(row.pid)
    ElMessage.success('删除成功')
    await fetchData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除人员失败:', error)
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
