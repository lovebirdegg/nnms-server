<template>
  <div class="head-container">
    <!-- 搜索 -->
##search_fields##
##filter_fields##
    <el-button class="filter-item" size="mini" type="primary" icon="el-icon-search" @click="toQuery">搜索</el-button>
    <div style="display: inline-block;margin: 0px 2px;">
      <el-button-group>
        <el-button v-if="checkPermission(['admin','device_all','device_delete'])" class="filter-item" size="mini" type="primary" @click="getPtoggleSelect">全选</el-button>
        <el-button v-if="checkPermission(['admin','device_all','device_delete'])" class="filter-item" size="mini" type="danger" @click="deleteSelect">删除</el-button>
        <el-button class="filter-item" size="mini" type="primary" @click="refresh">刷新</el-button>
        <el-button
          v-if="checkPermission(['admin','dict_all','dict_create'])"
          class="filter-item"
          size="mini"
          type="primary"
          icon="el-icon-plus"
          @click="$refs.form.dialog = true">新增</el-button>
        <eForm ref="form" :is-add="true"/>
      </el-button-group>
    </div>
    <br>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission' // 权限判断函数
import { getKey } from '@/api/dict'
import eForm from './form'

// 查询条件
export default {
  components: { eForm },
  props: {
    query: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      delLoading: false,
      updateLoading: false,
    }
  },
  created() {
    this.$nextTick(() => {
    })
  },
  methods: {
    checkPermission,
    toQuery() {
      this.$parent.page = 1
      this.$parent.init()
    },
    to() {
      const _this = this.$refs.form
      _this.dialog = true
    },
    getPtoggleSelect() {
      this.$parent.toggleSelection(this.$parent.data)
    },
    deleteSelect() {
      if (this.$parent.multipleSelection) {
        const count = this.$parent.multipleSelection.length
        this.$confirm('此操作将删除' + count + '条数据, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$parent.doSelectionDel()
          this.$message({
            type: 'success',
            message: '删除成功!'
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          })
        })
      } else {
        this.$message({
          type: 'info',
          message: '请先选择数据'
        })
      }
    },
    refresh() {
      this.$parent.init()
    },
    // 数据转换
    formatJson(filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => {
        if (j === 'Succeed') {
          return v[j] ? '成功' : '失败'
        } else {
          return v[j]
        }
      }))
    }
  }
}
</script>
