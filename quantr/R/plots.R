#' Plots the LCS and reference time-series
#'
#' @param data Data frame containing the low-cost sensor and reference measurements.
#' @param lcs_column The name of the column holding the LCS measurements.
#' @param reference_column The name of the column holding the reference measurements.
#' @param time_column The name of the column holding the time-stamps, which must be stored as datetime objects.
#' @return A plot stored as a \code{ggplot} object. If not assigned then prints the plot.
#' @family plots
#'
#' @examples
#' # Create dummy data frame
#' n_vals <- 100
#' df <- data.frame(timestamp=seq.POSIXt(from=as.POSIXct("2020-09-24 09:00:00"),
#'                                       to=as.POSIXct("2020-09-30 09:00:00"),
#'                                       length.out=n_vals),
#'                  ref=rnorm(n_vals, 30, 5),
#'                  lowcost=rnorm(n_vals, 32, 8))
#'
#' # Plot time-series
#' plot_time_series(df, lcs_column="lowcost", reference_column="ref", time_column="timestamp")
#' @export
plot_time_series <- function(data, lcs_column="lcs", reference_column="reference", time_column="time") {
    data |>
        dplyr::rename(lcs = lcs_column,
               reference = reference_column,
               time = time_column) |>
        tidyr::pivot_longer(c(lcs, reference), names_to="type") |>
        dplyr::mutate(type = factor(type, levels=c("lcs", "reference"),
                             labels=c("LCS", "Reference"))) |>
        ggplot2::ggplot() +
            ggplot2::geom_line(ggplot2::aes(x=time, y=value, colour=type), na.rm=T, alpha=0.8) +
            ggplot2::scale_colour_manual("", values=c("Black", "Red")) +
            ggplot2::theme_bw() +
            ggplot2::guides(colour="none") +
            ggplot2::theme(
                panel.grid.minor = ggplot2::element_blank()
            ) +
            ggplot2::labs(x="", y="Concentration")
}

#' Plots a scatter plot of the LCS measurements against the reference alongside accompanying statistics
#'
#' @inheritParams plot_time_series
#' @return A plot stored as a \code{ggplot} object. If not assigned then prints the plot.
#' @family plots
#' @examples
#' # Create dummy data frame
#' n_vals <- 100
#' df <- data.frame(timestamp=seq.POSIXt(from=as.POSIXct("2020-09-24 09:00:00"),
#'                                       to=as.POSIXct("2020-09-30 09:00:00"),
#'                                       length.out=n_vals),
#'                  ref=rnorm(n_vals, 30, 5),
#'                  lowcost=rnorm(n_vals, 32, 8))
#'
#' plot_scatter(df, lcs_column="lowcost", reference_column="ref")
#' @export
plot_scatter <- function(data, lcs_column="lcs", reference_column="reference") {
    data <- data |>
        dplyr::rename(lcs = lcs_column,
                      reference = reference_column)

    # Fit linear model
    mod <- stats::lm(lcs ~ reference, data=data)

    # Derive model statistics
    r2 <- summary(mod)$r.squared
    rmse <- sqrt(mean((data$reference - data$lcs)**2, na.rm=T))

    # Neatly format for plot
    eq <- sprintf("*y* = %.2f*x* %s %.1f", coef(mod)[2], ifelse(sign(coef(mod)[1]) == 1, "+", ""), coef(mod)[1])
    r2_label <- sprintf("*R*<sup>2</sup> = %.2f", r2)
    rmse_label <- sprintf("RMSE = %.2f", rmse)
    label <- sprintf("%s<br>%s<br>%s", eq, r2_label, rmse_label)

    data |>
        ggplot2::ggplot(ggplot2::aes(x=reference, y=lcs)) +
        ggpointdensity::geom_pointdensity(na.rm=T) +
        ggplot2::geom_abline(slope=1, intercept=0, colour="steelblue", size=0.7) +
        ggplot2::geom_abline(slope=coef(mod)[2], intercept=coef(mod)[1], colour="red", size=0.7) +
        ggplot2::scale_x_continuous(expand=ggplot2::expansion(c(0, 0.5))) +
        ggplot2::scale_y_continuous(expand=ggplot2::expansion(c(0, 0.5))) +
        ggtext::geom_richtext(ggplot2::aes(x=-Inf, y=Inf, label=label), data=data.frame(label=label), fill=NA, label.color=NA, vjust=1.1, hjust=0, size=4) +
        ggplot2::theme_bw() +
        ggplot2::coord_fixed() +
        ggplot2::scale_colour_viridis_c() +
        ggplot2::guides(colour="none") +
        ggplot2::theme(
            panel.grid.minor = ggplot2::element_blank(),
            axis.title.x = ggplot2::element_text(size=10)
        ) +
        ggplot2::labs(x="[Reference]", y="[LCS]")
}


#' Bland-Altman plot comparing the agreement between the LCS and the reference.
#'
#' @inheritParams plot_time_series
#' @return A plot stored as a \code{ggplot} object. If not assigned then prints the plot.
#' @family plots
#' @examples
#' # Create dummy data frame
#' n_vals <- 100
#' df <- data.frame(timestamp=seq.POSIXt(from=as.POSIXct("2020-09-24 09:00:00"),
#'                                       to=as.POSIXct("2020-09-30 09:00:00"),
#'                                       length.out=n_vals),
#'                  ref=rnorm(n_vals, 30, 5),
#'                  lowcost=rnorm(n_vals, 32, 8))
#'
#' plot_bland_altman(df, lcs_column="lowcost", reference_column="ref")
#' @export
plot_bland_altman <- function(data, lcs_column="lcs", reference_column="reference") {
    data <- data |>
        dplyr::rename(lcs = lcs_column,
               reference = reference_column)

    limits <- data |>
        dplyr::mutate(error = reference - lcs, avg = (reference + lcs) / 2) |>
        dplyr::summarise(mean = mean(error, na.rm=T),
                  sd = sd(error, na.rm=T)) |>
        dplyr::mutate(lower = mean - 1.96 * sd,
               upper = mean + 1.96 * sd)

    data |>
        dplyr::mutate(error = reference - lcs, avg = (reference + lcs) / 2) |>
        ggplot2::ggplot(ggplot2::aes(x=avg, y=error)) +
            ggpointdensity::geom_pointdensity(na.rm=T) +
            ggplot2::geom_hline(ggplot2::aes(yintercept=lower), data=limits, linetype="dashed", colour="red") +
            ggplot2::geom_hline(ggplot2::aes(yintercept=mean), data=limits, linetype="dashed", colour="steelblue") +
            ggplot2::geom_hline(ggplot2::aes(yintercept=upper), data=limits, linetype="dashed", colour="red") +
            ggplot2::scale_colour_viridis_c() +
            ggplot2::guides(colour="none") +
            ggplot2::theme_bw() +
            ggplot2::theme(
                panel.grid.minor = ggplot2::element_blank(),
                axis.title.x = ggplot2::element_text(size=10)
            ) +
            ggplot2::labs(x="Average Reference and LCS", y="Error (reference - lcs)")
}


#' Plot of Relative Expanded Uncertainty (REU) against reference concentrations.
#'
#' @inheritParams plot_time_series
#' @param LV The Limit Value for the species being plotted. If provided then a vertical line is drawn in red at this concentration.
#' @param DQO The relative uncertainty of the Data Quality Objective for this species. If provided then a horizontal line in blue is drawn at this relative uncertainty.
#' @param y_limits Particularly at low concentration values, REU curves can have large outliers that detract from the main trends.
#'  This option allows for the specification of the y-axis limits to zoom in to the region of interest. If \code{NULL} then no limits are applied.
#' @param smooth Whether to add a non-linear smooth to summarise the relationship between REU and concentration.
#' @return A plot stored as a \code{ggplot} object. If not assigned then prints the plot.
#' @family plots
#' @examples
#' # Create dummy data frame
#' n_vals <- 100
#' df <- data.frame(timestamp=seq.POSIXt(from=as.POSIXct("2020-09-24 09:00:00"),
#'                                       to=as.POSIXct("2020-09-30 09:00:00"),
#'                                       length.out=n_vals),
#'                  ref=rnorm(n_vals, 30, 5),
#'                  lowcost=rnorm(n_vals, 32, 8))
#'
#' # Remove the y-axis limits to show the large relative uncertainity of this imaginary device
#' plot_reu(df, lcs_column="lowcost", reference_column="ref", y_limits=NULL)
#'
#' # Add in the LV and DQO
#' plot_reu(df, lcs_column="lowcost", reference_column="ref", y_limits=NULL, LV=50, DQO=40)
#' @export
plot_reu <- function(data, lcs_column="lcs", reference_column="reference", LV=NULL, DQO=NULL, y_limits=c(0, 200), smooth=TRUE) {
    p <- data |>
        dplyr::rename(lcs = lcs_column,
               reference = reference_column) |>
        dplyr::mutate(reu = reu(reference, lcs)) |>
        ggplot2::ggplot(ggplot2::aes(x=reference, y=reu)) +
            ggpointdensity::geom_pointdensity() +
            ggplot2::scale_colour_viridis_c() +
            ggplot2::guides(colour="none") +
            ggplot2::labs(x="[Reference]",
                          y="REU (%)") +
            ggplot2::theme_bw() +
            ggplot2::theme(
                axis.title.x = ggplot2::element_text(size=10)
            )
    if (!is.null(LV) & is.numeric(LV)) {
        p <- p +
            ggplot2::geom_vline(xintercept = LV, linetype="dashed", colour="red")
    }
    if (!is.null(DQO) & is.numeric(DQO)) {
        p <- p +
            ggplot2::geom_hline(yintercept = DQO, linetype="dashed", colour="steelblue")
    }
    if (smooth) {
       p <- p +
            ggplot2::stat_smooth(se = FALSE)
    }
    if (!is.null(y_limits)) {
        p <- p +
            ggplot2::ylim(y_limits)
    }

    p
}
