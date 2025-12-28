// ============================================================================
// script.js - Client-side functionality for searching questions and managing exams
// Created: 2025-12-28 10:05:33 UTC
// ============================================================================

// ============================================================================
// SEARCH FUNCTIONALITY
// ============================================================================

/**
 * Initialize search functionality for questions
 */
function initializeSearchQuestions() {
  const searchInput = document.getElementById('searchInput');
  const searchBtn = document.getElementById('searchBtn');
  const clearBtn = document.getElementById('clearBtn');
  
  if (!searchInput) return;
  
  // Search on button click
  if (searchBtn) {
    searchBtn.addEventListener('click', performSearch);
  }
  
  // Clear search on button click
  if (clearBtn) {
    clearBtn.addEventListener('click', clearSearch);
  }
  
  // Search on Enter key press
  searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      performSearch();
    }
  });
  
  // Real-time search as user types (with debounce)
  let searchTimeout;
  searchInput.addEventListener('input', (e) => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      performSearch();
    }, 300);
  });
}

/**
 * Perform search on questions
 */
function performSearch() {
  const searchInput = document.getElementById('searchInput');
  const searchQuery = searchInput.value.trim().toLowerCase();
  const questionsList = document.getElementById('questionsList');
  
  if (!questionsList) return;
  
  const questions = questionsList.querySelectorAll('.question-item');
  let matchCount = 0;
  
  // Filter questions based on search query
  questions.forEach((question) => {
    const title = question.querySelector('.question-title')?.textContent.toLowerCase() || '';
    const description = question.querySelector('.question-description')?.textContent.toLowerCase() || '';
    const tags = question.querySelector('.question-tags')?.textContent.toLowerCase() || '';
    
    const isMatch = title.includes(searchQuery) || 
                    description.includes(searchQuery) || 
                    tags.includes(searchQuery);
    
    if (searchQuery === '' || isMatch) {
      question.style.display = '';
      matchCount++;
    } else {
      question.style.display = 'none';
    }
  });
  
  // Show/hide no results message
  displaySearchResults(matchCount, searchQuery);
}

/**
 * Clear search input and display all questions
 */
function clearSearch() {
  const searchInput = document.getElementById('searchInput');
  if (searchInput) {
    searchInput.value = '';
    searchInput.focus();
  }
  performSearch();
}

/**
 * Display search results feedback
 */
function displaySearchResults(matchCount, query) {
  let noResultsMsg = document.getElementById('noResultsMessage');
  
  if (matchCount === 0 && query !== '') {
    if (!noResultsMsg) {
      noResultsMsg = document.createElement('div');
      noResultsMsg.id = 'noResultsMessage';
      noResultsMsg.className = 'alert alert-info';
      const questionsList = document.getElementById('questionsList');
      if (questionsList) {
        questionsList.parentNode.insertBefore(noResultsMsg, questionsList);
      }
    }
    noResultsMsg.textContent = `No questions found for: "${query}"`;
    noResultsMsg.style.display = '';
  } else if (noResultsMsg) {
    noResultsMsg.style.display = 'none';
  }
}

// ============================================================================
// EXAM MANAGEMENT FUNCTIONALITY
// ============================================================================

/**
 * Initialize exam management features
 */
function initializeExamManagement() {
  initializeExamCreation();
  initializeExamEditing();
  initializeExamDeletion();
  initializeExamFiltering();
  initializeQuestionSelection();
}

/**
 * Initialize exam creation form
 */
function initializeExamCreation() {
  const createExamForm = document.getElementById('createExamForm');
  
  if (!createExamForm) return;
  
  createExamForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const examName = document.getElementById('examName')?.value.trim();
    const examDescription = document.getElementById('examDescription')?.value.trim();
    const examDuration = document.getElementById('examDuration')?.value;
    const selectedQuestions = getSelectedQuestions();
    
    // Validation
    if (!examName) {
      showAlert('Please enter an exam name', 'warning');
      return;
    }
    
    if (!examDuration || examDuration <= 0) {
      showAlert('Please enter a valid duration', 'warning');
      return;
    }
    
    if (selectedQuestions.length === 0) {
      showAlert('Please select at least one question', 'warning');
      return;
    }
    
    // Prepare exam data
    const examData = {
      name: examName,
      description: examDescription,
      duration: parseInt(examDuration),
      questions: selectedQuestions,
      createdAt: new Date().toISOString()
    };
    
    // Submit exam creation
    submitExamCreation(examData);
  });
}

/**
 * Submit exam creation via API
 */
function submitExamCreation(examData) {
  fetch('/api/exams/create', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(examData)
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      showAlert('Exam created successfully!', 'success');
      document.getElementById('createExamForm').reset();
      // Reload exams list
      loadExams();
    } else {
      showAlert(data.message || 'Failed to create exam', 'danger');
    }
  })
  .catch(error => {
    console.error('Error creating exam:', error);
    showAlert('Error creating exam. Please try again.', 'danger');
  });
}

/**
 * Get selected questions from checkboxes
 */
function getSelectedQuestions() {
  const checkboxes = document.querySelectorAll('input[name="questions"]:checked');
  return Array.from(checkboxes).map(checkbox => checkbox.value);
}

/**
 * Initialize exam editing functionality
 */
function initializeExamEditing() {
  const editExamButtons = document.querySelectorAll('.btn-edit-exam');
  
  editExamButtons.forEach(button => {
    button.addEventListener('click', (e) => {
      const examId = button.dataset.examId;
      loadExamForEditing(examId);
    });
  });
}

/**
 * Load exam data for editing
 */
function loadExamForEditing(examId) {
  fetch(`/api/exams/${examId}`)
    .then(response => response.json())
    .then(exam => {
      populateEditForm(exam);
      showEditModal(exam.id);
    })
    .catch(error => {
      console.error('Error loading exam:', error);
      showAlert('Error loading exam data', 'danger');
    });
}

/**
 * Populate edit form with exam data
 */
function populateEditForm(exam) {
  document.getElementById('editExamId').value = exam.id;
  document.getElementById('editExamName').value = exam.name;
  document.getElementById('editExamDescription').value = exam.description;
  document.getElementById('editExamDuration').value = exam.duration;
  
  // Update question selections
  const checkboxes = document.querySelectorAll('input[name="editQuestions"]');
  checkboxes.forEach(checkbox => {
    checkbox.checked = exam.questions.includes(checkbox.value);
  });
}

/**
 * Show edit exam modal
 */
function showEditModal(examId) {
  const editModal = document.getElementById('editExamModal');
  if (editModal) {
    editModal.style.display = 'block';
  }
}

/**
 * Initialize exam deletion functionality
 */
function initializeExamDeletion() {
  const deleteExamButtons = document.querySelectorAll('.btn-delete-exam');
  
  deleteExamButtons.forEach(button => {
    button.addEventListener('click', (e) => {
      const examId = button.dataset.examId;
      const examName = button.dataset.examName;
      
      if (confirm(`Are you sure you want to delete the exam "${examName}"?`)) {
        deleteExam(examId);
      }
    });
  });
}

/**
 * Delete exam via API
 */
function deleteExam(examId) {
  fetch(`/api/exams/${examId}`, {
    method: 'DELETE'
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      showAlert('Exam deleted successfully!', 'success');
      loadExams();
    } else {
      showAlert(data.message || 'Failed to delete exam', 'danger');
    }
  })
  .catch(error => {
    console.error('Error deleting exam:', error);
    showAlert('Error deleting exam. Please try again.', 'danger');
  });
}

/**
 * Initialize exam filtering functionality
 */
function initializeExamFiltering() {
  const filterInput = document.getElementById('filterExams');
  
  if (!filterInput) return;
  
  filterInput.addEventListener('input', (e) => {
    const filterText = e.target.value.toLowerCase();
    const examItems = document.querySelectorAll('.exam-item');
    
    examItems.forEach(exam => {
      const examName = exam.querySelector('.exam-name')?.textContent.toLowerCase() || '';
      const examDescription = exam.querySelector('.exam-description')?.textContent.toLowerCase() || '';
      
      const isMatch = examName.includes(filterText) || examDescription.includes(filterText);
      exam.style.display = isMatch ? '' : 'none';
    });
  });
}

/**
 * Initialize question selection functionality
 */
function initializeQuestionSelection() {
  const selectAllCheckbox = document.getElementById('selectAllQuestions');
  
  if (!selectAllCheckbox) return;
  
  selectAllCheckbox.addEventListener('change', (e) => {
    const isChecked = e.target.checked;
    const checkboxes = document.querySelectorAll('input[name="questions"]');
    
    checkboxes.forEach(checkbox => {
      checkbox.checked = isChecked;
    });
  });
}

/**
 * Load and display exams
 */
function loadExams() {
  fetch('/api/exams')
    .then(response => response.json())
    .then(data => {
      displayExams(data.exams);
    })
    .catch(error => {
      console.error('Error loading exams:', error);
      showAlert('Error loading exams', 'danger');
    });
}

/**
 * Display exams in the UI
 */
function displayExams(exams) {
  const examsList = document.getElementById('examsList');
  
  if (!examsList) return;
  
  if (exams.length === 0) {
    examsList.innerHTML = '<p class="text-center text-muted">No exams found.</p>';
    return;
  }
  
  examsList.innerHTML = exams.map(exam => `
    <div class="exam-item card mb-3">
      <div class="card-body">
        <h5 class="card-title exam-name">${escapeHtml(exam.name)}</h5>
        <p class="card-text exam-description">${escapeHtml(exam.description)}</p>
        <div class="exam-meta">
          <small class="text-muted">Duration: ${exam.duration} minutes</small>
          <small class="text-muted"> | Questions: ${exam.questions.length}</small>
        </div>
        <div class="exam-actions mt-3">
          <button class="btn btn-sm btn-primary btn-edit-exam" data-exam-id="${exam.id}">
            Edit
          </button>
          <button class="btn btn-sm btn-danger btn-delete-exam" data-exam-id="${exam.id}" data-exam-name="${escapeHtml(exam.name)}">
            Delete
          </button>
        </div>
      </div>
    </div>
  `).join('');
  
  // Re-initialize event listeners
  initializeExamEditing();
  initializeExamDeletion();
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/**
 * Show alert message
 */
function showAlert(message, type = 'info') {
  const alertDiv = document.createElement('div');
  alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
  alertDiv.role = 'alert';
  alertDiv.innerHTML = `
    ${message}
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
  `;
  
  const alertContainer = document.getElementById('alertContainer') || document.body;
  alertContainer.insertBefore(alertDiv, alertContainer.firstChild);
  
  // Auto-dismiss after 5 seconds
  setTimeout(() => {
    alertDiv.remove();
  }, 5000);
}

/**
 * Escape HTML special characters
 */
function escapeHtml(text) {
  const map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  };
  return text.replace(/[&<>"']/g, m => map[m]);
}

/**
 * Format date to readable format
 */
function formatDate(dateString) {
  const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
  return new Date(dateString).toLocaleDateString('en-US', options);
}

/**
 * Validate email format
 */
function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

/**
 * Debounce function for optimized event handling
 */
function debounce(func, delay) {
  let timeoutId;
  return function (...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
      func.apply(this, args);
    }, delay);
  };
}

// ============================================================================
// INITIALIZATION
// ============================================================================

/**
 * Initialize all functionality when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', () => {
  // Initialize search functionality
  initializeSearchQuestions();
  
  // Initialize exam management
  initializeExamManagement();
  
  // Load exams on page load
  if (document.getElementById('examsList')) {
    loadExams();
  }
  
  console.log('✓ Script.js initialized successfully');
});

// Export functions for external use if needed
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    performSearch,
    clearSearch,
    initializeExamManagement,
    submitExamCreation,
    deleteExam,
    loadExams,
    showAlert,
    escapeHtml,
    formatDate,
    isValidEmail,
    debounce
  };
}
