// Tooltips
var tooltipTriggerList = [].slice.call(
  document.querySelectorAll('[data-bs-toggle="tooltip"]')
);
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl);
});

// Edit video content
const remakeBtn = $("#remake-btn");

const originalThread = { comments: {} };
const editedThread = { comments: {} };

const remakeBtnVisibility = () => {
  !("body" in editedThread) && Object.keys(editedThread.comments).length === 0
    ? remakeBtn.attr("disabled", true)
    : remakeBtn.attr("disabled", false);
};

// Edit body
const body = $("#body-text");
const editBodyBtn = $("#edit-body-btn");
const confirmBodyContainer = $("#confirm-body-container");
const confirmBodyBtn = $("#confirm-body-btn");

const inputBody = () => {
  // Disable confirm button if body is unchanged
  var text;

  editedThread.body ? (text = editedThread.body) : (text = originalThread.body);

  confirmBodyBtn.attr("disabled", body.text() === text);
};

const editBody = () => {
  if (editBodyBtn.text() === "Edit") {
    // Add body to originalThread if it doesn't exist
    if (!("body" in originalThread)) originalThread["body"] = body.text();

    body.attr("contenteditable", true);
    body.addClass("editable-content");
    body.focus();

    confirmBodyContainer.attr("hidden", false);
    editBodyBtn.text("Cancel");
  } else {
    // Resets body
    body.text(editedThread.body || originalThread.body);

    body.attr("contenteditable", false);
    body.removeClass("editable-content");

    confirmBodyContainer.attr("hidden", true);
    confirmBodyBtn.attr("disabled", true);
    editBodyBtn.text("Edit");
  }
};

const confirmBody = () => {
  // Check if changed body is the same as the original
  body.text() === originalThread.body
    ? delete editedThread.body
    : (editedThread.body = body.text());

  body.attr("contenteditable", false);
  body.removeClass("editable-content");

  confirmBodyContainer.attr("hidden", true);
  confirmBodyBtn.attr("disabled", true);
  editBodyBtn.text("Edit");

  remakeBtnVisibility();
};

// Edit comment
const inputComment = (commentId) => {
  const comment = $(`#${commentId} #comment-text`);
  const confirmBtn = $(`#${commentId} #confirm-btn`);

  // Disable confirm button if comment is unchanged
  var text;

  editedThread.comments[commentId]
    ? (text = editedThread.comments[commentId])
    : (text = originalThread.comments[commentId]);

  confirmBtn.attr("disabled", comment.text() === text);
};

const editComment = (commentId) => {
  const comment = $(`#${commentId} #comment-text`);
  const editBtn = $(`#${commentId} #edit-btn`);
  const confirmContainer = $(`#${commentId} #confirm-container`);
  const confirmBtn = $(`#${commentId} #confirm-btn`);

  if (editBtn.text() === "Edit") {
    // Add comment to originalThread if it doesn't exist
    if (!(commentId in originalThread.comments))
      originalThread.comments[commentId] = comment.text();

    comment.attr("contenteditable", true);
    comment.addClass("editable-content");
    comment.focus();

    confirmContainer.attr("hidden", false);
    editBtn.text("Cancel");
  } else {
    // Resets comment
    commentId in editedThread.comments
      ? comment.text(editedThread.comments[commentId])
      : comment.text(originalThread.comments[commentId]);

    comment.attr("contenteditable", false);
    comment.removeClass("editable-content");

    confirmContainer.attr("hidden", true);
    confirmBtn.attr("disabled", true);
    editBtn.text("Edit");
  }
};

const confirmComment = (commentId) => {
  const comment = $(`#${commentId} #comment-text`);
  const editBtn = $(`#${commentId} #edit-btn`);
  const confirmContainer = $(`#${commentId} #confirm-container`);
  const confirmBtn = $(`#${commentId} #confirm-btn`);

  // Check if changed comment is the same as the original
  comment.text() === originalThread.comments[commentId]
    ? delete editedThread.comments[commentId]
    : (editedThread.comments[commentId] = comment.text());

  comment.attr("contenteditable", false);
  comment.removeClass("editable-content");

  confirmContainer.attr("hidden", true);
  confirmBtn.attr("disabled", true);
  editBtn.text("Edit");

  remakeBtnVisibility();
};

const queueRemake = (subreddit, thread) => {
  $.ajax({
    url: `/queue_remake/${subreddit}/${thread}`,
    type: "POST",
    dataType: "json",
    data: JSON.stringify(editedThread),
    contentType: "application/json",
    success: () => {
      window.location.href = "/";
    },
  });
};
