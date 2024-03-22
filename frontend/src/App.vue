<template>
  <div class="app">
    <nav class="navbar" style="align-items: center;margin-bottom: 50px;">
      <ul style="justify-content:center;align-items: center;">
        <li :class="{ 'active': activeTab === 'home' }" @click="activeTab = 'home'">Home</li>
        <li :class="{ 'active': activeTab === 'upload' }" @click="activeTab = 'upload'">Upload</li>
      </ul>
    </nav>
    <div v-if="activeTab === 'home'" class="content" style="margin-top: 50px;">
      <div class="animation">
        <h1>
          <span v-for="(char, index) in text" :key="index" :class="{ 'bold': index === boldIndex }">{{ char }}</span>
          <span class="dot" :class="{ 'blink': isDotVisible }">.</span>
        </h1>
      </div>
      <footer class="footer" style="margin-top: 240px;">
      <div class="footer-content">
        <p>Connect with me:</p>
        <ul>
          <li><a href="https://www.linkedin.com/in/vishal-s-murali" target="_blank">LinkedIn</a></li>
          <li><a href="https://www.instagram.com/your-instagram" target="_blank">Instagram</a></li>
        </ul>
        <p>For inquiries, contact:</p>
        <ul>
          <li>Mobile: +91 9066146109</li>
          <li>Email: vishalsmurali@gmail.com</li>
        </ul>
      </div>
    </footer>
    </div>
    <div v-else-if="activeTab === 'upload'" class="content">
      <form @submit.prevent="uploadFile">
        <input type="file" ref="fileInput" accept="image/*">
        <button type="submit" class="upload-button">Upload</button>
      </form>
    </div>
    <div v-else-if="activeTab === 'response'" class="content">
      <div class="response-container">
        <div class="image-container">
          <img :src="imageData" alt="Uploaded Image">
          <button @click="downloadImage" class="download-button">Download Image</button>
        </div>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>Vehicle Type</th>
                <th>Count</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(count, key) in vehicleCounts" :key="key">
                <td>{{ key }}</td>
                <td>{{ count }}</td>
              </tr>
            </tbody>
          </table>
          <button @click="exportToExcel" class="export-button">Export to Excel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import * as XLSX from 'xlsx';
import FileSaver from 'file-saver';

export default {
  name: 'App',
  data() {
    return {
      isDotVisible: true,
      activeTab: 'home',
      text: '',
      boldIndex: 10, // Index where 'IISC' starts
      imageData: '',
      vehicleCounts: {}
    };
  },
  mounted() {
    this.animateText("Welcome to my IISC assignment");
    setInterval(() => {
      this.isDotVisible = !this.isDotVisible;
    }, 1000);
  },
  methods: {
    animateText(text) {
      let i = 0;
      const interval = setInterval(() => {
        if (i >= text.length) {
          clearInterval(interval);
          return;
        }
        this.text += text[i];
        i++;
      }, 100);
    },
    uploadFile() {
      const file = this.$refs.fileInput.files[0];
      if (file) {
        const formData = new FormData();
        formData.append('image', file);

        axios.post('http://localhost:5000/classify', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        .then(response => {
          console.log('Response from server:', response.data);
          this.imageData = 'data:image/jpeg;base64,' + response.data.image;
          this.vehicleCounts = response.data.count;
          this.activeTab = 'response'; // Switch to the response tab
        })
        .catch(error => {
          console.error('Error uploading file:', error);
          // Handle error here
        });
      } else {
        console.log('No file selected.');
      }
    },
    downloadImage() {
      const filename = 'uploaded_image.jpg';
      const blob = this.dataURLtoBlob(this.imageData);
      FileSaver.saveAs(blob, filename);
    },
    dataURLtoBlob(dataURL) {
      const arr = dataURL.split(',');
      const mime = arr[0].match(/:(.*?);/)[1];
      const bstr = atob(arr[1]);
      let n = bstr.length;
      const u8arr = new Uint8Array(n);
      while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
      }
      return new Blob([u8arr], { type: mime });
    },
    exportToExcel() {
      const wb = XLSX.utils.book_new();
      const ws = XLSX.utils.json_to_sheet(this.generateTableData());
      XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');
      const excelBuffer = XLSX.write(wb, { bookType: 'xlsx', type: 'array' });
      const filename = 'table_data.xlsx';
      this.saveExcelFile(excelBuffer, filename);
    },
    generateTableData() {
      const data = [];
      for (const [key, value] of Object.entries(this.vehicleCounts)) {
        data.push({ 'Vehicle Type': key, 'Count': value });
      }
      return data;
    },
    saveExcelFile(buffer, filename) {
      const data = new Blob([buffer], { type: 'application/octet-stream' });
      FileSaver.saveAs(data, filename);
    }
  }
};
</script>

<style>
.footer {
  background-color: #333;
  color: #fff;
  padding: 20px;
}

.footer-content {
  text-align: center;
}

.footer p {
  margin-bottom: 10px;
}

.footer ul {
  padding: 0;
  list-style: none;
}

.footer ul li {
  margin-bottom: 5px;
}

.footer a {
  color: #fff;
  text-decoration: none;
}

.footer a:hover {
  text-decoration: underline;
}
.app {
  background-color: black;
  color: white;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.content {
  text-align: center;
}

.animation {
  position: relative;
}

.dot {
  width: 1px;
  height: 1px;
  background-color: white;
}

.blink {
  animation: blink-animation 0.8s step-end infinite;
}

@keyframes blink-animation {
  50% {
    opacity: 0;
  }
}

.navbar {
  background-color: #333;
  margin-bottom: 20px;
}

.navbar ul {
  list-style: none;
  padding: 0;
  display: flex;
}

.navbar ul li {
  margin-right: 20px;
  cursor: pointer;
}

.navbar ul li.active {
  border-bottom: 2px solid white;
}

.bold {
  font-weight: bold;
}

.response-container {
  display: flex;
}

.image-container {
  width: 50%; /* Adjust width as needed */
  height: auto;
  margin-right: 20px;
}

.image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.table-container {
  flex: 1; /* Take remaining space */
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 8px;
  border: 1px solid white;
}

th {
  background-color: #333;
  color: white;
}

tr:nth-child(even) {
  background-color: #555;
}

tr:hover {
  background-color: #777;
}

.upload-button, .download-button, .export-button {
  padding: 10px 20px;
  background-color: #007bff;
  border: none;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}

.upload-button:hover, .download-button:hover, .export-button:hover {
  background-color: #0056b3;
}

.upload-button:active, .download-button:active, .export-button:active {
  background-color: #0056b3;
}

.upload-button:focus, .download-button:focus, .export-button:focus {
  outline: none;
}
</style>