document.addEventListener("DOMContentLoaded", function () {
    var script = document.createElement("script");
    script.src = "https://cdn.tiny.cloud/1/no-api-key/tinymce/6/skins/ui/oxide/content.min.css";
    script.referrerpolicy = "origin";
    script.onload = function () {
        tinymce.init({
            selector: '#id_content',  // Target the Django admin textarea
            height: 400,  // Set desired height
            menubar: true,
            valid_elements: '*[*]', // Allow all HTML elements  
            plugins: [
                // Core editing features
                'anchor', 'autolink', 'charmap', 'codesample', 'emoticons', 'image', 'link', 'lists', 'media', 'searchreplace', 'table', 'visualblocks', 'wordcount',
                // Your account includes a free trial of TinyMCE premium features
                // Try the most popular premium features until Apr 3, 2025:
                'checklist', 'mediaembed', 'casechange', 'export', 'formatpainter', 'pageembed', 'a11ychecker', 'tinymcespellchecker', 'permanentpen', 'powerpaste', 'advtable', 'advcode', 'editimage', 'advtemplate', 'ai', 'mentions', 'tinycomments', 'tableofcontents', 'footnotes', 'mergetags', 'autocorrect', 'typography', 'inlinecss', 'markdown','importword', 'exportword', 'exportpdf'
              ],
            toolbar: 'undo redo | formatselect | bold italic backcolor | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | removeformat | link image | code',
            // content_css: "/static/blogHome/css/tinymce.css", // Optional custom CSS
            branding: false,  // Removes "Powered by Tiny"
            image_advtab: true,  // Enables advanced image options
            automatic_uploads: true,
            file_picker_types: 'image',
            file_picker_callback: function (cb, value, meta) {
                var input = document.createElement('input');
                input.setAttribute('type', 'file');
                input.setAttribute('accept', 'image/*');
                input.onchange = function () {
                    var file = this.files[0];
                    var reader = new FileReader();
                    reader.onload = function () {
                        cb(reader.result, { title: file.name });
                    };
                    reader.readAsDataURL(file);
                };
                input.click();
            }
        });
    };
    document.head.appendChild(script);
});
