#' Calculates the Relative Expanded Uncertainty of low-cost sensor measurements when compared with a reference instrument.
#'
#' @param ref Reference measurements
#' @param lcs Low-cost-sensor measurements
#' @param k Multiplier of standard error in relative uncertainty to obtain the expanded uncertainty. Defaults to 2 standard deviations.
#' @param u_ref Relative uncertainty of the reference instrument
#' @return A vector of the same length as \code{ref} and \code{lcs} containing the corresponding REU estimates.
#' @examples
#' # Create dummy data frame
#' n_vals <- 100
#' df <- data.frame(timestamp=seq.POSIXt(from=as.POSIXct("2020-09-24 09:00:00"),
#'                                       to=as.POSIXct("2020-09-30 09:00:00"),
#'                                       length.out=n_vals),
#'                  ref=rnorm(n_vals, 30, 5),
#'                  lowcost=rnorm(n_vals, 32, 8))
#'
#' reu(df$ref, df$lowcost)
#'
#' @export
reu <- function(ref, lcs, k=2, u_ref = 0) {
    stopifnot(length(ref) == length(lcs))

    # Setup to pairwise complete observations
    available <- !is.na(lcs) & !is.na(ref)
    n <- sum(available)
    lcs <- lcs[available]
    ref <- ref[available]

    # Fit linear model and obtain derived statistics
    mod <- lm(lcs ~ ref)
    rss <- sum(mod$residuals**2)
    sigma_v_sqr <- rss / (n-2)

    # error variance due to the deviation of the 1:1 line
    ec <- (coef(mod)[1] + (coef(mod)[2] - 1)*ref)**2

    # Combine into Relative Expanded Uncertainty
    k*((sigma_v_sqr - u_ref**2 + ec)**(1/2))*100/lcs
}
