(function() {

  // Save the elements in jQuery variables
  var categoryFormEl = $('.js-article-sorting_category-form');
  var categoryInputEl = $('.js-article-sorting_category-input');
  var errorTextEl = $('.js-article-sorting_error-text');
  var articlesResultsEl = $('.js-article-sorting_article-results');
  var articlesTableEl = $('.js-article-sorting_article-table');

  // Handle the category form submit
  categoryFormEl.submit(function(e) {

    // Prevent the default browser submit of the form.
    e.preventDefault();

    // Empty the results table
    articlesTableEl.empty();

    // If the category input is not valid, don't continue with the submit
    var categoryValue = categoryInputEl.val();
    if (!_validateCategoryInput(categoryValue)) {
      return;
    }

    // Submit the category to the server to get the article results
    _getArticlesInCategory(categoryValue);
  })

  // Remove the error message as soon as the user starts typing
  categoryInputEl.on('keyup', function() {
    errorTextEl.empty().hide();
    categoryInputEl.removeClass('is-invalid');
  })

  function _validateCategoryInput(categoryValue) {
    // Do basic validation: The category input should have at least 2 characters or more
    if (categoryValue.length < 2) {
      categoryInputEl.addClass('is-invalid');
      errorTextEl.show().text('You better add a valid text');
      return false;
    }

    return true;
  }

  function _getArticlesInCategory() {
    // Make the request to the get_articles_in_category endpoint
    $.ajax({
      url: 'get_articles_in_category',
      data: {
          'category_title': categoryInputEl.val()
        },
      success: function(response) {

        // TODO: deal with no response

         // Loop over the article results and add a table row for every article
         for (i = 0; i < response.category_page_extracts.length; i++) {
           var tableRow =
             '<tr class="toggle-parent-' + i + '" data-toggle="collapse" data-target=".js-article-sorting_text-extract' + i + '">' +
               '<td>' + response.category_page_extracts[i]['title'] + '</td>' +
               '<td>' + response.category_page_extracts[i]['readability_scores']['FleschReadingEase'] + '</td>' +
             '</tr>' +
             '<tr>' +
               '<td colspan=2>' +
                 '<div class="collapse js-article-sorting_text-extract' + i + '" data-parent=".toggle-parent-' + i + '">' +
                  response.category_page_extracts[i]['extract'] +
                 '</div>' +
               '</td>' +
             '</tr>';
           articlesTableEl.append(tableRow);
         }
         articlesResultsEl.removeAttr('hidden');

      },
      fail: function() {
        // In case there was a failure, show an error message
        errorTextEl.show().text('Something went wrong with the submit. Please try again');
      }
    })
  }

}())