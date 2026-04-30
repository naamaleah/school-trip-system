const API_BASE = "http://127.0.0.1:8000";

const resultsDiv = document.getElementById("results");
const teacherActions = document.getElementById("teacher-actions");
const teacherAccessCard = document.getElementById("teacher-access-card");

let verifiedTeacher = null;
let map;
let studentMarkers = [];
let teacherMarker = null;
let farStudentIds = new Set();

function getCurrentTimeISO() {
  return new Date().toISOString().split(".")[0] + "Z";
}

async function postJson(url, body) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.detail || "Request failed");
  }

  return data;
}

function requireVerifiedTeacher() {
  if (!verifiedTeacher) {
    showMessage("Please verify a teacher first.", true);
    return null;
  }
  return verifiedTeacher;
}

function showMessage(message, isError = false) {
  resultsDiv.innerHTML = `
    <div class="alert ${isError ? "alert-danger" : "alert-info"}">
      ${message}
    </div>
  `;
}

function renderUsers(list, type) {
  if (!list || list.length === 0) {
    showMessage(`No ${type.toLowerCase()}s found.`);
    return;
  }

  resultsDiv.innerHTML = list.map(item => `
    <div class="card p-2 mb-2">
      <h6>${type}</h6>
      <p><b>Name:</b> ${item.first_name} ${item.last_name}</p>
      <p><b>ID:</b> ${item.id}</p>
      <p><b>Class:</b> ${item.class_name}</p>
    </div>
  `).join("");
}

function renderFarStudents(list) {
  if (!list || list.length === 0) {
    showMessage("All students are within 3 km.");
    return;
  }

  resultsDiv.innerHTML = list.map(student => `
    <div class="card p-2 mb-2 border-danger">
      <p><b>${student.first_name} ${student.last_name}</b></p>
      <p>ID: ${student.id}</p>
      <p>Class: ${student.class_name}</p>
      <p>Distance: ${student.distance_km} km</p>
    </div>
  `).join("");
}

function renderSingleUser(item, type) {
  resultsDiv.innerHTML = `
    <div class="card p-2">
      <h6>${type}</h6>
      <p><b>Name:</b> ${item.first_name} ${item.last_name}</p>
      <p><b>ID:</b> ${item.id}</p>
      <p><b>Class:</b> ${item.class_name}</p>
    </div>
  `;
}

document.getElementById("register-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const type = document.getElementById("register-type").value;

  const userData = {
    first_name: document.getElementById("register-first-name").value,
    last_name: document.getElementById("register-last-name").value,
    id: document.getElementById("register-id").value,
    class_name: document.getElementById("register-class").value
  };

  const endpoint = type === "teacher" ? "/teachers" : "/students";

  try {
    const data = await postJson(`${API_BASE}${endpoint}`, userData);
    renderSingleUser(data, "Registered");
    e.target.reset();
  } catch (error) {
    showMessage(error.message, true);
  }
});

document.getElementById("verify-teacher").addEventListener("click", async () => {
  const teacherData = {
    id: document.getElementById("access-teacher-id").value,
    first_name: document.getElementById("access-teacher-first-name").value,
    last_name: document.getElementById("access-teacher-last-name").value
  };

  try {
    const data = await postJson(`${API_BASE}/teacher-access`, teacherData);

    verifiedTeacher = teacherData;
    farStudentIds = new Set();

    teacherAccessCard.classList.add("d-none");
    teacherActions.classList.remove("d-none");

    showMessage(`Teacher verified: ${data.first_name} ${data.last_name}`);

    await loadTeacherLocation();
    await loadStudentLocations();

  } catch (error) {
    verifiedTeacher = null;
    farStudentIds = new Set();

    clearTeacherMarker();
    await loadStudentLocations();

    teacherAccessCard.classList.remove("d-none");
    teacherActions.classList.add("d-none");

    showMessage(error.message, true);
  }
});

document.getElementById("load-teachers").addEventListener("click", async () => {
  const teacher = requireVerifiedTeacher();
  if (!teacher) return;

  const data = await postJson(`${API_BASE}/teachers/all`, teacher);
  renderUsers(data, "Teacher");
});

document.getElementById("load-students").addEventListener("click", async () => {
  const teacher = requireVerifiedTeacher();
  if (!teacher) return;

  const data = await postJson(`${API_BASE}/students/all`, teacher);
  renderUsers(data, "Student");
});

document.getElementById("find-teacher").addEventListener("click", async () => {
  const teacher = requireVerifiedTeacher();
  if (!teacher) return;

  const teacherId = document.getElementById("find-teacher-id").value;

  const data = await postJson(`${API_BASE}/teachers/find`, {
    requesting_teacher: teacher,
    teacher_id: teacherId
  });

  renderSingleUser(data, "Teacher");
});

document.getElementById("find-student").addEventListener("click", async () => {
  const teacher = requireVerifiedTeacher();
  if (!teacher) return;

  const studentId = document.getElementById("find-student-id").value;

  const data = await postJson(`${API_BASE}/students/find`, {
    requesting_teacher: teacher,
    student_id: studentId
  });

  renderSingleUser(data, "Student");
});

document.getElementById("load-my-students").addEventListener("click", async () => {
  const teacher = requireVerifiedTeacher();
  if (!teacher) return;

  const data = await postJson(`${API_BASE}/teachers/students`, {
    requesting_teacher: teacher,
    teacher_id: teacher.id
  });

  renderUsers(data, "Student");
});

document.getElementById("check-far-students").addEventListener("click", async () => {
  const teacher = requireVerifiedTeacher();
  if (!teacher) return;

  const data = await postJson(`${API_BASE}/teachers/far-students`, {
    requesting_teacher: teacher,
    teacher_id: teacher.id
  });

  farStudentIds = new Set(data.map(student => student.id));

  renderFarStudents(data);

  await loadStudentLocations();
  await loadTeacherLocation();
});

document.getElementById("logout-teacher").addEventListener("click", async () => {
  verifiedTeacher = null;
  farStudentIds = new Set();

  clearTeacherMarker();
  await loadStudentLocations();

  teacherActions.classList.add("d-none");
  teacherAccessCard.classList.remove("d-none");

  showMessage("Logged out");
});

document.getElementById("update-location").addEventListener("click", async () => {
  const type = document.getElementById("location-type").value;

  const locationData = {
    ID: document.getElementById("location-id").value,
    Coordinates: {
      Longitude: {
        Degrees: document.getElementById("long-deg").value,
        Minutes: document.getElementById("long-min").value,
        Seconds: document.getElementById("long-sec").value
      },
      Latitude: {
        Degrees: document.getElementById("lat-deg").value,
        Minutes: document.getElementById("lat-min").value,
        Seconds: document.getElementById("lat-sec").value
      }
    },
    Time: getCurrentTimeISO()
  };

  const endpoint = type === "teacher"
    ? "/locations/teacher"
    : "/locations/student";

  try {
    await postJson(`${API_BASE}${endpoint}`, locationData);

    showMessage(
      `${type === "teacher" ? "Teacher" : "Student"} location updated successfully`
    );

    if (type === "student") {
      await loadStudentLocations();
    }

    if (type === "teacher" && verifiedTeacher && verifiedTeacher.id === locationData.ID) {
      await loadTeacherLocation();
    }

  } catch (error) {
    showMessage(error.message, true);
  }
});

function initMap() {
  if (!map) {
    map = L.map("map").setView([31.778, 35.235], 11);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "&copy; OpenStreetMap"
    }).addTo(map);
  }
}

function clearStudentMarkers() {
  studentMarkers.forEach(marker => map.removeLayer(marker));
  studentMarkers = [];
}

function clearTeacherMarker() {
  if (teacherMarker) {
    map.removeLayer(teacherMarker);
    teacherMarker = null;
  }
}

async function loadStudentLocations() {
  const res = await fetch(`${API_BASE}/locations/students`);
  const locations = await res.json();

  initMap();
  clearStudentMarkers();

  locations.forEach(loc => {
    const isFar = farStudentIds.has(loc.student_id);

    const marker = L.circleMarker([loc.latitude, loc.longitude], {
      radius: 8,
      color: isFar ? "red" : "green",
      fillColor: isFar ? "red" : "green",
      fillOpacity: 0.8
    }).addTo(map);

    marker.bindPopup(`Student ${loc.student_id}`);
    studentMarkers.push(marker);
  });
}

async function loadTeacherLocation() {
  const teacher = requireVerifiedTeacher();
  if (!teacher) return;

  try {
    const location = await postJson(`${API_BASE}/locations/teacher/current`, {
      requesting_teacher: teacher,
      teacher_id: teacher.id
    });

    initMap();
    clearTeacherMarker();

    teacherMarker = L.circleMarker([location.latitude, location.longitude], {
      radius: 10,
      color: "blue",
      fillColor: "blue",
      fillOpacity: 0.9
    }).addTo(map);

    teacherMarker.bindPopup(`Teacher ${teacher.first_name} ${teacher.last_name}`);

  } catch (error) {
    clearTeacherMarker();
  }
}

initMap();
loadStudentLocations();